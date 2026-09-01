<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->libdir . '/resourcelib.php');
require_once(__DIR__ . '/course_definition.php');
require_once(__DIR__ . '/source_activity.php');
$definition = load_course_definition($argv[1] ?? '');
$identity = $definition['identity'];
if ($DB->record_exists('course', ['shortname' => $identity['shortname']])) {
    fwrite(STDERR, "Course already exists; reset with bin/course-package down.\n");
    exit(1);
}
$course = create_course((object) [
    'fullname' => $identity['fullname'], 'shortname' => $identity['shortname'],
    'category' => 1, 'format' => $definition['settings']['format'],
    'numsections' => count($definition['modules']), 'visible' => 0, 'enablecompletion' => 1,
    'summary' => $identity['summary'],
    'summaryformat' => FORMAT_HTML,
]);
course_create_sections_if_missing($course, count($definition['modules']));
$general = $DB->get_record('course_sections', ['course' => $course->id, 'section' => 0], '*', MUST_EXIST);
course_update_section($course, $general, ['name' => $definition['general']['name'], 'summary' => course_html($definition['general']['introduction']), 'summaryformat' => FORMAT_HTML]);
foreach ($definition['modules'] as $moduleIndex => $moduleDefinition) {
    $sectionNumber = $moduleIndex + 1;
    $section = $DB->get_record('course_sections', ['course' => $course->id, 'section' => $sectionNumber], '*', MUST_EXIST);
    course_update_section($course, $section, ['name' => $moduleDefinition['name'], 'summary' => course_html($moduleDefinition['introduction']), 'summaryformat' => FORMAT_HTML]);
    foreach ($moduleDefinition['activities'] as $activity) {
        $content = render_source_activity($activity);
        add_moduleinfo((object) [
            'course' => $course->id, 'module' => $DB->get_field('modules', 'id', ['name' => 'page'], MUST_EXIST),
            'modulename' => 'page', 'section' => $sectionNumber, 'name' => $activity['name'],
            'intro' => '', 'introformat' => FORMAT_HTML, 'content' => $content, 'contentformat' => FORMAT_HTML,
            'display' => RESOURCELIB_DISPLAY_OPEN, 'printintro' => 0, 'printlastmodified' => 0,
            'completion' => COMPLETION_TRACKING_MANUAL, 'completionview' => 0, 'visible' => 1,
        ], $course);
    }
}
rebuild_course_cache($course->id, true);
echo "Generated hidden Course from Course Definition.\n";
echo "COURSE_ID={$course->id}\n";
