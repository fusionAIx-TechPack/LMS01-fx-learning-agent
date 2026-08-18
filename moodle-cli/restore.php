<?php
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/backup/util/includes/restore_includes.php');
require_once(__DIR__ . '/course_definition.php');
$package = $argv[1] ?? null;
$definition = load_course_definition($argv[2] ?? '');
$shortname = $definition['identity']['shortname'];
if (!$package || !is_readable($package)) { fwrite(STDERR, "Course Package is missing or unreadable.\n"); exit(66); }
if ($DB->record_exists('course', ['shortname' => $shortname])) {
    fwrite(STDERR, "Restore target is not clean; reset it with bin/course-package down.\n"); exit(1);
}
$backupid = restore_controller::get_tempdir_name(SITEID, 2);
$directory = make_backup_temp_directory($backupid);
$packer = get_file_packer('application/vnd.moodle.backup');
if (!$packer->extract_to_pathname($package, $directory)) throw new RuntimeException('Moodle could not unpack the Course Package.');
$targetcourseid = restore_dbops::create_new_course($definition['identity']['fullname'], $shortname, 1);
$controller = new restore_controller($backupid, $targetcourseid, backup::INTERACTIVE_NO, backup::MODE_GENERAL, 2, backup::TARGET_NEW_COURSE);
$controller->execute_precheck();
$precheck = $controller->get_precheck_results();
if (isset($precheck['errors'])) throw new RuntimeException('Moodle restore precheck failed: ' . json_encode($precheck));
if (!empty($precheck)) echo 'Restore precheck warnings: ' . json_encode($precheck) . PHP_EOL;
$controller->execute_plan();
$courseid = $controller->get_courseid();
$controller->destroy();
echo "Restored Course as ID {$courseid}.\n";
