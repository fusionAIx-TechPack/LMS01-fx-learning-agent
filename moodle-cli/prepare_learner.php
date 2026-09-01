<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once($CFG->libdir . '/enrollib.php');
require_once(__DIR__ . '/course_definition.php');

$definition = load_course_definition($argv[1] ?? '');
$course = $DB->get_record('course', ['shortname' => $definition['identity']['shortname']], '*', MUST_EXIST);
$username = 'course-package-learner';
$password = 'Local-Learner-2026';

if ($DB->record_exists('user', ['username' => $username])) {
    throw new RuntimeException('The isolated learner already exists; reset with bin/course-package down.');
}

$userid = user_create_user((object) [
    'auth' => 'manual',
    'confirmed' => 1,
    'mnethostid' => $CFG->mnet_localhost_id,
    'username' => $username,
    'password' => $password,
    'firstname' => 'Course Package',
    'lastname' => 'Learner',
    'email' => 'course-package-learner@example.invalid',
], true, false);

$studentrole = $DB->get_record('role', ['shortname' => 'student'], '*', MUST_EXIST);
$manual = enrol_get_plugin('manual');
$manualinstance = null;
foreach (enrol_get_instances($course->id, true) as $instance) {
    if ($instance->enrol === 'manual') {
        $manualinstance = $instance;
        break;
    }
}
if (!$manual) {
    throw new RuntimeException('The isolated Moodle does not provide the standard manual enrolment plugin.');
}
if (!$manualinstance) {
    $instanceid = $manual->add_instance($course);
    $manualinstance = $DB->get_record('enrol', ['id' => $instanceid], '*', MUST_EXIST);
}
$manual->enrol_user($manualinstance, $userid, $studentrole->id);

// Grant the capabilities exercised by the isolated learner HTTP acceptance
// check explicitly at Course scope. This does not modify the packaged Course.
$coursecontext = context_course::instance($course->id);
foreach (['mod/page:view', 'mod/url:view', 'mod/assign:view', 'mod/assign:submit', 'mod/forum:viewdiscussion', 'moodle/course:togglecompletion'] as $capability) {
    assign_capability($capability, CAP_ALLOW, $studentrole->id, $coursecontext->id, true);
}

// The packaged Course is already visible; force it here as well so this isolated
// restored Course can be exercised through an HTTP learner session regardless of
// the package's stored visibility.
$DB->set_field('course', 'visible', 1, ['id' => $course->id]);
rebuild_course_cache($course->id, true);

$modules = array_values($DB->get_records('course_modules', ['course' => $course->id], 'id'));
if (count($modules) !== 5) {
    throw new RuntimeException('The restored Course does not have the expected five activities.');
}
[$overview, $resources, $videos, $assignment, $discussion] = $modules;

$structure = $definition['structure'];
$acts = $structure['activities'];

echo "COURSE_ID={$course->id}\n";
echo "ACTIVITY_ID={$overview->id}\n";
echo "OVERVIEW_CMID={$overview->id}\n";
echo "RESOURCES_CMID={$resources->id}\n";
echo "VIDEOS_CMID={$videos->id}\n";
echo "ASSIGNMENT_CMID={$assignment->id}\n";
echo "DISCUSSION_CMID={$discussion->id}\n";
echo "LEARNER_ID={$userid}\n";
echo "LEARNER_USERNAME={$username}\n";
echo "LEARNER_PASSWORD={$password}\n";
echo 'PRIMARY_URL_BASE64=' . base64_encode($acts['resources']['primary_url']) . "\n";
echo 'EXPECTED_TEXT_BASE64=' . base64_encode($definition['identity']['fullname']) . "\n";
echo 'EXPECTED_TEXT_BASE64=' . base64_encode($structure['section_name']) . "\n";
foreach (['overview', 'resources', 'videos', 'assignment', 'discussion'] as $key) {
    echo 'EXPECTED_TEXT_BASE64=' . base64_encode($acts[$key]['name']) . "\n";
}
