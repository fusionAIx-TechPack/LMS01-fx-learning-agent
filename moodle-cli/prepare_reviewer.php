<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once($CFG->libdir . '/enrollib.php');
require_once(__DIR__ . '/course_definition.php');

$definition = load_course_definition($argv[1] ?? '');
$course = $DB->get_record('course', ['shortname' => $definition['identity']['shortname']], '*', MUST_EXIST);
$username = 'course-review-learner';
$password = 'LocalOnly-Review1!';

if ($DB->record_exists('user', ['username' => $username])) {
    throw new RuntimeException('The isolated review learner already exists; reset with bin/course-package down.');
}

$userid = user_create_user((object) [
    'auth' => 'manual',
    'confirmed' => 1,
    'mnethostid' => $CFG->mnet_localhost_id,
    'username' => $username,
    'password' => $password,
    'firstname' => 'Course Review',
    'lastname' => 'Learner',
    'email' => 'course-review-learner@example.invalid',
], true, false);

$studentrole = $DB->get_record('role', ['shortname' => 'student'], '*', MUST_EXIST);
$manual = enrol_get_plugin('manual');
if (!$manual) {
    throw new RuntimeException('The isolated Moodle does not provide the standard manual enrolment plugin.');
}
$manualinstance = null;
foreach (enrol_get_instances($course->id, true) as $instance) {
    if ($instance->enrol === 'manual') {
        $manualinstance = $instance;
        break;
    }
}
if (!$manualinstance) {
    $instanceid = $manual->add_instance($course);
    $manualinstance = $DB->get_record('enrol', ['id' => $instanceid], '*', MUST_EXIST);
}
$manual->enrol_user($manualinstance, $userid, $studentrole->id);

// The disposable reviewer is enrolled as a learner and receives the standard
// manager role only so the hidden Course is reviewable. User and role
// assignments are excluded from the user-data-free Course Package; unlike
// course-scoped capability overrides, they do not change packaged Course
// configuration.
$coursecontext = context_course::instance($course->id);
$managerrole = $DB->get_record('role', ['shortname' => 'manager'], '*', MUST_EXIST);
role_assign($managerrole->id, $userid, $coursecontext->id);
rebuild_course_cache($course->id, true);

echo "REVIEWER_USERNAME={$username}\n";
echo "REVIEWER_PASSWORD={$password}\n";
