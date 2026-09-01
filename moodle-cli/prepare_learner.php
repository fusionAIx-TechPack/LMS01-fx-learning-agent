<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once($CFG->libdir . '/enrollib.php');
require_once(__DIR__ . '/course_definition.php');

$definition = load_course_definition($argv[1] ?? '');
$course = $DB->get_record('course', ['shortname' => $definition['identity']['shortname']], '*', MUST_EXIST);
$username = 'course-package-learner';
$password = 'LocalOnly-Learner1!';

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
assign_capability('mod/page:view', CAP_ALLOW, $studentrole->id, $coursecontext->id, true);
assign_capability('moodle/course:togglecompletion', CAP_ALLOW, $studentrole->id, $coursecontext->id, true);

// Package visibility was verified while hidden. Publish only this isolated restored
// Course so its learner-visible behavior can now be exercised through HTTP.
$DB->set_field('course', 'visible', 1, ['id' => $course->id]);
rebuild_course_cache($course->id, true);

$activityid = array_values($DB->get_records('course_modules', ['course' => $course->id], 'id'))[0]->id ?? null;
if (!$activityid) {
    throw new RuntimeException('The restored Course has no Learning Activity for the learner check.');
}

echo "COURSE_ID={$course->id}\n";
echo "ACTIVITY_ID={$activityid}\n";
echo "LEARNER_ID={$userid}\n";
echo "LEARNER_USERNAME={$username}\n";
echo "LEARNER_PASSWORD={$password}\n";
echo 'EXPECTED_TEXT_BASE64=' . base64_encode($definition['identity']['fullname']) . "\n";
echo 'EXPECTED_TEXT_BASE64=' . base64_encode($definition['general']['name']) . "\n";
echo 'SOURCE_URL_BASE64=' . base64_encode($definition['modules'][0]['activities'][0]['source']['url']) . "\n";
foreach ($definition['modules'] as $module) {
    echo 'EXPECTED_TEXT_BASE64=' . base64_encode($module['name']) . "\n";
    foreach ($module['activities'] as $activity) {
        echo 'EXPECTED_TEXT_BASE64=' . base64_encode($activity['name']) . "\n";
    }
}
