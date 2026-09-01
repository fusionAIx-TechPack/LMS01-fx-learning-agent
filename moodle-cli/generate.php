<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->libdir . '/resourcelib.php');
require_once($CFG->libdir . '/completionlib.php');
require_once(__DIR__ . '/course_definition.php');
require_once(__DIR__ . '/activity_content.php');

$definition = load_course_definition($argv[1] ?? '');
$identity = $definition['identity'];
if ($DB->record_exists('course', ['shortname' => $identity['shortname']])) {
    fwrite(STDERR, "Course already exists; reset with bin/course-package down.\n");
    exit(1);
}
$structure = $definition['structure'];
$acts = $structure['activities'];

// newsitems is pinned to 0 so the site's course default does not make
// mod_forum add an "Announcements" forum: the generated Course must contain
// exactly the five fixed activities and nothing else.
// The Course has exactly one section: section 0, the always-present top section,
// named for the Course topic and holding all five activities. numsections is 0
// so there is no additional (empty) section below it.
// The Course is created visible so it restores visible on production import;
// the disposable review Moodle is not internet-facing.
$course = create_course((object) [
    'fullname' => $identity['fullname'], 'shortname' => $identity['shortname'],
    'category' => 1, 'format' => $definition['settings']['format'],
    'numsections' => 0, 'visible' => (int) $definition['settings']['visible'], 'enablecompletion' => 1,
    'newsitems' => 0,
    'summary' => $identity['summary'],
    'summaryformat' => FORMAT_HTML,
]);
course_create_sections_if_missing($course, 0);

$section = $DB->get_record('course_sections', ['course' => $course->id, 'section' => 0], '*', MUST_EXIST);
course_update_section($course, $section, [
    'name' => $structure['section_name'],
    'summary' => course_html($structure['section_introduction']),
    'summaryformat' => FORMAT_HTML,
]);

$pageModuleId = $DB->get_field('modules', 'id', ['name' => 'page'], MUST_EXIST);
$urlModuleId = $DB->get_field('modules', 'id', ['name' => 'url'], MUST_EXIST);
$assignModuleId = $DB->get_field('modules', 'id', ['name' => 'assign'], MUST_EXIST);
$forumModuleId = $DB->get_field('modules', 'id', ['name' => 'forum'], MUST_EXIST);

$overviewHtml = render_overview_page($acts['overview']);
$overview = add_moduleinfo((object) [
    'course' => $course->id, 'module' => $pageModuleId, 'modulename' => 'page', 'section' => 0,
    'name' => $acts['overview']['name'],
    'intro' => $overviewHtml, 'introformat' => FORMAT_HTML,
    'content' => $overviewHtml, 'contentformat' => FORMAT_HTML,
    'display' => RESOURCELIB_DISPLAY_OPEN, 'printintro' => 0, 'printlastmodified' => 0,
    'showdescription' => 1,
    'completion' => COMPLETION_TRACKING_MANUAL, 'completionview' => 0, 'visible' => 1,
], $course);

// A bare link that opens the entered main URL in a new window
// (RESOURCELIB_DISPLAY_NEW). No description.
$resources = add_moduleinfo((object) [
    'course' => $course->id, 'module' => $urlModuleId, 'modulename' => 'url', 'section' => 0,
    'name' => $acts['resources']['name'],
    'externalurl' => $acts['resources']['primary_url'],
    'intro' => '', 'introformat' => FORMAT_HTML,
    'display' => RESOURCELIB_DISPLAY_NEW, 'printintro' => 0,
    'parameters' => '', 'showdescription' => 0,
    'completion' => COMPLETION_TRACKING_MANUAL, 'completionview' => 0, 'visible' => 1,
], $course);

$videosHtml = render_videos_page($acts['videos']);
$videos = add_moduleinfo((object) [
    'course' => $course->id, 'module' => $pageModuleId, 'modulename' => 'page', 'section' => 0,
    'name' => $acts['videos']['name'],
    'intro' => $videosHtml, 'introformat' => FORMAT_HTML,
    'content' => $videosHtml, 'contentformat' => FORMAT_HTML,
    'display' => RESOURCELIB_DISPLAY_OPEN, 'printintro' => 0, 'printlastmodified' => 0,
    'showdescription' => 0,
    'completion' => COMPLETION_TRACKING_MANUAL, 'completionview' => 0, 'visible' => 1,
], $course);

$assignment = add_moduleinfo((object) [
    'course' => $course->id, 'module' => $assignModuleId, 'modulename' => 'assign', 'section' => 0,
    'name' => $acts['assignment']['name'],
    'intro' => render_assignment_intro($acts['assignment']), 'introformat' => FORMAT_HTML,
    'alwaysshowdescription' => 1,
    'submissiondrafts' => 0, 'requiresubmissionstatement' => 0,
    'sendnotifications' => 0, 'sendlatenotifications' => 0, 'sendstudentnotifications' => 0,
    'duedate' => 0, 'cutoffdate' => 0, 'gradingduedate' => 0, 'allowsubmissionsfromdate' => 0,
    'grade' => 0, 'teamsubmission' => 0, 'requireallteammemberssubmit' => 0,
    'blindmarking' => 0, 'markingworkflow' => 0, 'markingallocation' => 0, 'markinganonymous' => 0,
    'hidegrader' => 0, 'attemptreopenmethod' => 'none', 'maxattempts' => -1,
    'timelimit' => 0, 'submissionattachments' => 0, 'preventsubmissionnotingroup' => 0,
    'assignsubmission_onlinetext_enabled' => 0,
    'assignsubmission_file_enabled' => 1,
    'assignsubmission_file_maxfiles' => (int) $acts['assignment']['max_files'],
    'assignsubmission_file_maxsizebytes' => 0,
    'assignsubmission_file_filetypes' => (string) $acts['assignment']['file_types'],
    'assignsubmission_comments_enabled' => 0,
    'assignfeedback_comments_enabled' => 0,
    'assignfeedback_file_enabled' => 0,
    'assignfeedback_offline_enabled' => 0,
    'assignfeedback_editpdf_enabled' => 0,
    'completion' => COMPLETION_TRACKING_AUTOMATIC, 'completionview' => 0,
    'completionusegrade' => 0, 'completionsubmit' => 1,
    'visible' => 1,
], $course);

// A general discussion forum at the bottom, not graded, manual completion.
$discussion = add_moduleinfo((object) [
    'course' => $course->id, 'module' => $forumModuleId, 'modulename' => 'forum', 'section' => 0,
    'name' => $acts['discussion']['name'],
    'intro' => render_discussion_intro($acts['discussion']), 'introformat' => FORMAT_HTML,
    'type' => 'general',
    'forcesubscribe' => 0, 'trackingtype' => 1,
    'maxbytes' => 512000, 'maxattachments' => 3,
    'assessed' => 0, 'scale' => 0, 'grade_forum' => 0,
    'blockafter' => 0, 'blockperiod' => 0, 'warnafter' => 0,
    'duedate' => 0, 'cutoffdate' => 0,
    'completiondiscussions' => 0, 'completionreplies' => 0, 'completionposts' => 0,
    'showdescription' => 1,
    'completion' => COMPLETION_TRACKING_MANUAL, 'completionview' => 0, 'visible' => 1,
], $course);

rebuild_course_cache($course->id, true);
echo "Generated Course from Course Definition.\n";
echo "COURSE_ID={$course->id}\n";
echo "OVERVIEW_CMID={$overview->coursemodule}\n";
echo "RESOURCES_CMID={$resources->coursemodule}\n";
echo "VIDEOS_CMID={$videos->coursemodule}\n";
echo "ASSIGNMENT_CMID={$assignment->coursemodule}\n";
echo "DISCUSSION_CMID={$discussion->coursemodule}\n";
