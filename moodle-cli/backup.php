<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/backup/util/includes/backup_includes.php');
$destination = $argv[1] ?? null;
require_once(__DIR__ . '/course_definition.php');
$definition = load_course_definition($argv[2] ?? '');
if (!$destination) { fwrite(STDERR, "Missing backup destination.\n"); exit(64); }
$course = $DB->get_record('course', ['shortname' => $definition['identity']['shortname']], '*', MUST_EXIST);
$controller = new backup_controller(backup::TYPE_1COURSE, $course->id, backup::FORMAT_MOODLE, backup::INTERACTIVE_NO, backup::MODE_GENERAL, 2);
foreach (['users', 'anonymize', 'role_assignments', 'comments', 'badges', 'calendarevents', 'userscompletion', 'logs', 'grade_histories'] as $name) {
    if ($controller->get_plan()->setting_exists($name)) $controller->get_plan()->get_setting($name)->set_value(0);
}
$controller->execute_plan();
$file = $controller->get_results()['backup_destination'] ?? null;
if (!$file) throw new RuntimeException('Moodle did not produce a backup file.');
$file->copy_content_to($destination);
$controller->destroy();
echo "Created user-data-free Moodle backup.\n";
