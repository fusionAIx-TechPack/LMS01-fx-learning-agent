import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/course_proposal.dart';
import '../models/job_status.dart';

class ApiService {
  // Default base URL for backend service
  final String baseUrl;

  ApiService({this.baseUrl = 'http://localhost:8088/api'});

  /// Analyze raw URLs (or single URL) to generate proposal card(s)
  Future<List<CourseProposal>> analyzeUrls(List<String> urls) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/analyze-urls'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'urls': urls}),
      ).timeout(const Duration(seconds: 15));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List;
        return data.map((item) => CourseProposal.fromJson(item)).toList();
      }
    } catch (_) {
      // Fallback: Return simulated proposal so UI can be demonstrated standalone
    }
    return _mockProposals(urls);
  }

  /// Upload Excel or CSV file
  Future<List<CourseProposal>> uploadSpreadsheet(
    List<int> bytes,
    String fileName,
  ) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/upload-spreadsheet'),
      );
      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          bytes,
          filename: fileName,
        ),
      );

      var streamedResponse = await request.send().timeout(const Duration(seconds: 20));
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List;
        return data.map((item) => CourseProposal.fromJson(item)).toList();
      }
    } catch (_) {
      // Fallback mock for demo
    }

    return _mockProposals([
      'https://learn.microsoft.com/en-us/training/paths/ai-concepts-developers/',
      'https://academy.pega.com/topic/generative-ai-pega/v1',
    ]);
  }

  /// Start the Moodle course build process for confirmed proposal
  Future<GenerationJob> startBuild(CourseProposal proposal) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/jobs'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(proposal.toJson()),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        return GenerationJob.fromJson(jsonDecode(response.body));
      }
    } catch (_) {
      // Fallback mock job
    }

    final slug = proposal.courseName.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]+'), '-');
    return GenerationJob(
      jobId: 'job-${DateTime.now().millisecondsSinceEpoch}',
      courseSlug: slug,
      courseName: proposal.courseName,
      currentStep: BuildStep.scrapingUrl,
      progress: 0.15,
      logs: ['Job queued...', 'Connecting to Moodle environment...'],
      createdAt: DateTime.now(),
    );
  }

  /// Poll status of an ongoing generation job
  Future<GenerationJob?> pollJobStatus(String jobId) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/jobs/$jobId'));
      if (response.statusCode == 200) {
        return GenerationJob.fromJson(jsonDecode(response.body));
      }
    } catch (_) {
      // return null if backend unreachable
    }
    return null;
  }

  /// Retrieve list of completed courses and available .mbz downloads
  Future<List<CourseProposal>> getCompletedCourses() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/courses'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List;
        return data.map((item) => CourseProposal.fromJson(item)).toList();
      }
    } catch (_) {}
    return [];
  }

  /// Mock generator for seamless UI testing without a running backend
  List<CourseProposal> _mockProposals(List<String> urls) {
    return urls.map((url) {
      String inferredName = 'AI Concepts for Developers';
      String overview = 'Explain core AI concepts and terminology across generative AI and agents, NLP, computer vision, and retrieval-augmented generation.';
      int duration = 90;
      String level = 'beginner';
      String audience = 'Developers and technology professionals starting with AI';

      if (url.contains('pega')) {
        inferredName = 'Generative AI with Pega Constellation';
        overview = 'Learn to leverage generative AI features inside Pega workflows and build autonomous enterprise agent solutions.';
        duration = 120;
        level = 'intermediate';
        audience = 'Pega System Architects and Lead Decisioning Engineers';
      } else if (url.contains('banking') || url.contains('finance')) {
        inferredName = 'Financial Services AI Foundations';
        overview = 'Understand KYC, AML regulations and apply machine learning models to financial risk detection.';
        duration = 180;
        level = 'intermediate';
        audience = 'Financial Compliance Officers and Fintech Engineers';
      }

      return CourseProposal(
        id: 'prop-${DateTime.now().millisecondsSinceEpoch}-${url.hashCode}',
        sourceUrl: url,
        courseName: inferredName,
        courseOverview: overview,
        courseDurationMinutes: duration,
        level: level,
        language: 'en-US',
        audience: audience,
        moduleCount: 4,
        topics: [
          'Introduction and Core Terminology',
          'Foundational Models & Embeddings',
          'Enterprise Architecture & Guardrails',
          'Verification, Testing & Deployment',
        ],
        referenceVideos: [
          ReferenceVideoItem(
            title: 'Generative AI Architecture Overview',
            url: 'https://www.youtube.com/watch?v=sample1',
            publisher: 'TechTalks Official',
            note: 'Covers foundational concepts and transformer blocks',
          ),
          ReferenceVideoItem(
            title: 'Enterprise AI Security and Best Practices',
            url: 'https://www.youtube.com/watch?v=sample2',
            publisher: 'Cloud Academy',
            note: 'Walkthrough of data isolation and enterprise safety',
          ),
        ],
        status: 'pending',
      );
    }).toList();
  }
}
