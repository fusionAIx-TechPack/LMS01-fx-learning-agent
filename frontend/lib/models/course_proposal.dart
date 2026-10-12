import 'dart:convert';

class ReferenceVideoItem {
  final String title;
  final String url;
  final String publisher;
  final String note;

  ReferenceVideoItem({
    required this.title,
    required this.url,
    required this.publisher,
    required this.note,
  });

  factory ReferenceVideoItem.fromJson(Map<String, dynamic> json) {
    return ReferenceVideoItem(
      title: json['title'] ?? '',
      url: json['url'] ?? '',
      publisher: json['publisher'] ?? '',
      note: json['note'] ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
    'title': title,
    'url': url,
    'publisher': publisher,
    'note': note,
  };
}

class CourseProposal {
  final String id;
  final String sourceUrl;
  String courseName;
  String courseOverview;
  int courseDurationMinutes;
  String level; // 'beginner', 'intermediate', 'advanced'
  String language; // default 'en-US'
  String audience;
  int moduleCount;
  List<String> topics;
  List<ReferenceVideoItem> referenceVideos;
  bool isApproved;
  String status; // 'pending', 'approved', 'packaging', 'completed', 'failed'
  String? errorMessage;
  String? packagePath;

  CourseProposal({
    required this.id,
    required this.sourceUrl,
    required this.courseName,
    required this.courseOverview,
    required this.courseDurationMinutes,
    this.level = 'beginner',
    this.language = 'en-US',
    required this.audience,
    this.moduleCount = 1,
    this.topics = const [],
    this.referenceVideos = const [],
    this.isApproved = false,
    this.status = 'pending',
    this.errorMessage,
    this.packagePath,
  });

  factory CourseProposal.fromJson(Map<String, dynamic> json) {
    var rawVideos = json['reference_videos'] as List? ?? [];
    List<ReferenceVideoItem> videos = rawVideos
        .map((v) => ReferenceVideoItem.fromJson(v as Map<String, dynamic>))
        .toList();

    var rawTopics = json['topics'] as List? ?? [];
    List<String> topics = rawTopics.map((t) => t.toString()).toList();

    return CourseProposal(
      id: json['id'] ?? DateTime.now().millisecondsSinceEpoch.toString(),
      sourceUrl: json['source_url'] ?? '',
      courseName: json['course_name'] ?? 'Untitled Course',
      courseOverview: json['course_overview'] ?? '',
      courseDurationMinutes: json['course_duration_minutes'] ?? 60,
      level: json['level'] ?? 'beginner',
      language: json['language'] ?? 'en-US',
      audience: json['audience'] ?? 'General learners',
      moduleCount: json['module_count'] ?? (topics.isNotEmpty ? topics.length : 1),
      topics: topics,
      referenceVideos: videos,
      isApproved: json['is_approved'] ?? false,
      status: json['status'] ?? 'pending',
      errorMessage: json['error_message'],
      packagePath: json['package_path'],
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'source_url': sourceUrl,
    'course_name': courseName,
    'course_overview': courseOverview,
    'course_duration_minutes': courseDurationMinutes,
    'level': level,
    'language': language,
    'audience': audience,
    'module_count': moduleCount,
    'topics': topics,
    'reference_videos': referenceVideos.map((v) => v.toJson()).toList(),
    'is_approved': isApproved,
    'status': status,
    'error_message': errorMessage,
    'package_path': packagePath,
  };

  CourseProposal copyWith({
    String? id,
    String? sourceUrl,
    String? courseName,
    String? courseOverview,
    int? courseDurationMinutes,
    String? level,
    String? language,
    String? audience,
    int? moduleCount,
    List<String>? topics,
    List<ReferenceVideoItem>? referenceVideos,
    bool? isApproved,
    String? status,
    String? errorMessage,
    String? packagePath,
  }) {
    return CourseProposal(
      id: id ?? this.id,
      sourceUrl: sourceUrl ?? this.sourceUrl,
      courseName: courseName ?? this.courseName,
      courseOverview: courseOverview ?? this.courseOverview,
      courseDurationMinutes: courseDurationMinutes ?? this.courseDurationMinutes,
      level: level ?? this.level,
      language: language ?? this.language,
      audience: audience ?? this.audience,
      moduleCount: moduleCount ?? this.moduleCount,
      topics: topics ?? this.topics,
      referenceVideos: referenceVideos ?? this.referenceVideos,
      isApproved: isApproved ?? this.isApproved,
      status: status ?? this.status,
      errorMessage: errorMessage ?? this.errorMessage,
      packagePath: packagePath ?? this.packagePath,
    );
  }
}
