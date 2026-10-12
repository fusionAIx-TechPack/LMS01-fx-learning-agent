enum BuildStep {
  idle,
  scrapingUrl,
  synthesizingAi,
  compilingDefinition,
  instantiatingMoodle,
  packagingMbz,
  completed,
  failed,
}

extension BuildStepHelper on BuildStep {
  String get label {
    switch (this) {
      case BuildStep.idle:
        return 'Waiting to start';
      case BuildStep.scrapingUrl:
        return 'Extracting content from Source URL';
      case BuildStep.synthesizingAi:
        return 'AI synthesizing course brief & reference videos';
      case BuildStep.compilingDefinition:
        return 'Validating course definition schema';
      case BuildStep.instantiatingMoodle:
        return 'Configuring local Moodle container';
      case BuildStep.packagingMbz:
        return 'Building & verifying Moodle .mbz package';
      case BuildStep.completed:
        return 'Complete! Package is ready for download';
      case BuildStep.failed:
        return 'Build encountered an error';
    }
  }

  double get progressFraction {
    switch (this) {
      case BuildStep.idle:
        return 0.0;
      case BuildStep.scrapingUrl:
        return 0.20;
      case BuildStep.synthesizingAi:
        return 0.40;
      case BuildStep.compilingDefinition:
        return 0.60;
      case BuildStep.instantiatingMoodle:
        return 0.75;
      case BuildStep.packagingMbz:
        return 0.90;
      case BuildStep.completed:
        return 1.0;
      case BuildStep.failed:
        return 1.0;
    }
  }
}

class GenerationJob {
  final String jobId;
  final String courseSlug;
  final String courseName;
  final BuildStep currentStep;
  final double progress;
  final List<String> logs;
  final String? mbzDownloadUrl;
  final String? error;
  final DateTime createdAt;

  GenerationJob({
    required this.jobId,
    required this.courseSlug,
    required this.courseName,
    required this.currentStep,
    required this.progress,
    required this.logs,
    this.mbzDownloadUrl,
    this.error,
    required this.createdAt,
  });

  factory GenerationJob.fromJson(Map<String, dynamic> json) {
    BuildStep step = BuildStep.idle;
    String rawStep = json['step'] ?? '';
    for (var s in BuildStep.values) {
      if (s.name == rawStep) {
        step = s;
        break;
      }
    }

    var rawLogs = json['logs'] as List? ?? [];
    List<String> logs = rawLogs.map((e) => e.toString()).toList();

    return GenerationJob(
      jobId: json['job_id'] ?? '',
      courseSlug: json['course_slug'] ?? '',
      courseName: json['course_name'] ?? 'Course',
      currentStep: step,
      progress: (json['progress'] as num?)?.toDouble() ?? step.progressFraction,
      logs: logs,
      mbzDownloadUrl: json['mbz_download_url'],
      error: json['error'],
      createdAt: json['created_at'] != null 
          ? DateTime.parse(json['created_at']) 
          : DateTime.now(),
    );
  }
}
