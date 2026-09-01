<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once($CFG->libdir . '/enrollib.php');
require_once(__DIR__ . '/course_definition.php');

$definition = load_course_definition($argv[1] ?? '');
$course = $DB->get_record('course', ['shortname' => $definition['identity']['shortname']], '*', MUST_EXIST);
$username = 'course-review-learner';
// Disposable, local-only. The single `-` is the only non-alphanumeric character
// (Moodle's password policy needs one); no `!` or other shell/paste-hostile
// symbols.
$password = 'Local-Review-2026';

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

// The disposable reviewer is enrolled as a learner and also receives the
// standard manager role so the staged Course is reviewable. Moodle's freshly
// installed role defaults do not grant the learner the activity-view and manual
// completion capabilities this Course uses, so grant them to the standard
// student role at system scope in this disposable environment. System role
// capabilities plus user and role assignments are excluded from the
// user-data-free Course Package; course-scoped overrides would change packaged
// Course configuration.
$coursecontext = context_course::instance($course->id);
$managerrole = $DB->get_record('role', ['shortname' => 'manager'], '*', MUST_EXIST);
$systemcontext = context_system::instance();
foreach (['mod/page:view', 'mod/url:view', 'mod/assign:view', 'mod/forum:viewdiscussion', 'moodle/course:togglecompletion'] as $capability) {
    assign_capability($capability, CAP_ALLOW, $studentrole->id, $systemcontext->id, true);
}
role_assign($managerrole->id, $userid, $coursecontext->id);
rebuild_course_cache($course->id, true);

$activities = array_values($DB->get_records('course_modules', ['course' => $course->id], 'id', 'id, section, module'));
if (!$activities) {
    throw new RuntimeException('The review Course has no Learning Activity.');
}

echo "REVIEWER_USERNAME={$username}\n";
echo "REVIEWER_PASSWORD={$password}\n";
foreach ($activities as $activity) {
    $modname = $DB->get_field('modules', 'name', ['id' => $activity->module]);
    echo "REVIEW_ACTIVITY={$activity->id}:{$activity->section}:{$modname}\n";
}
