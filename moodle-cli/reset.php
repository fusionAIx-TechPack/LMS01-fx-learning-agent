<?php
// Fast-iteration reset: remove the prior generated Course and the disposable
// review/learner accounts from an existing Moodle install without dropping the
// database or reinstalling Moodle. Used by `bin/course-package ... --reuse` so
// repeated builds skip the multi-minute Moodle install. `bin/course-package
// down` remains the full, authoritative teardown.
define('CLI_SCRIPT', true);
require('/var/www/html/config.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once(__DIR__ . '/course_definition.php');

$definition = load_course_definition($argv[1] ?? '');
$shortname = $definition['identity']['shortname'];

if ($course = $DB->get_record('course', ['shortname' => $shortname])) {
    delete_course($course->id, false);
    echo "Removed existing Course {$shortname}.\n";
}

foreach (['course-review-learner', 'course-package-learner'] as $username) {
    if ($user = $DB->get_record('user', ['username' => $username, 'deleted' => 0])) {
        user_delete_user($user);
        echo "Removed disposable account {$username}.\n";
    }
}

echo "Moodle reset for reuse.\n";
