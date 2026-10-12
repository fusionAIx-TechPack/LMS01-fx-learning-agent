import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/course_proposal.dart';
import '../providers/course_generator_provider.dart';

class ReviewGateScreen extends StatefulWidget {
  const ReviewGateScreen({super.key});

  @override
  State<ReviewGateScreen> createState() => _ReviewGateScreenState();
}

class _ReviewGateScreenState extends State<ReviewGateScreen> {
  late TextEditingController _nameController;
  late TextEditingController _overviewController;
  late TextEditingController _durationController;
  late TextEditingController _audienceController;
  String _selectedLevel = 'beginner';

  @override
  void initState() {
    super.initState();
    final provider = context.read<CourseGeneratorProvider>();
    final proposal = provider.currentProposal;

    _nameController = TextEditingController(text: proposal?.courseName ?? '');
    _overviewController = TextEditingController(text: proposal?.courseOverview ?? '');
    _durationController = TextEditingController(
      text: proposal != null ? proposal.courseDurationMinutes.toString() : '60',
    );
    _audienceController = TextEditingController(text: proposal?.audience ?? '');
    _selectedLevel = proposal?.level ?? 'beginner';
  }

  void _syncControllersWithProposal(CourseProposal proposal) {
    _nameController.text = proposal.courseName;
    _overviewController.text = proposal.courseOverview;
    _durationController.text = proposal.courseDurationMinutes.toString();
    _audienceController.text = proposal.audience;
    _selectedLevel = proposal.level;
  }

  @override
  void dispose() {
    _nameController.dispose();
    _overviewController.dispose();
    _durationController.dispose();
    _audienceController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<CourseGeneratorProvider>();
    final proposal = provider.currentProposal;

    if (proposal == null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('No course proposal ready for review.'),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: () => provider.setTab(AppViewTab.input),
              child: const Text('Back to Input'),
            ),
          ],
        ),
      );
    }

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 960),
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(vertical: 24),
          child: Card(
            elevation: 8,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: BorderSide(color: Colors.white.withOpacity(0.08)),
            ),
            color: const Color(0xFF131B2E),
            child: Padding(
              padding: const EdgeInsets.all(32.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Top Gate Banner
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.amber.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.amber.withOpacity(0.4)),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.verified_user_outlined, color: Colors.amberAccent, size: 28),
                        const SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text(
                                'Human Review & Approval Gate',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.amberAccent,
                                  fontSize: 16,
                                ),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                'Inspect or tweak the AI-derived learning metadata below before packaging into Moodle.',
                                style: TextStyle(color: Colors.grey.shade300, fontSize: 13),
                              ),
                            ],
                          ),
                        ),
                        if (provider.proposals.length > 1)
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                            decoration: BoxDecoration(
                              color: const Color(0xFF1E293B),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(
                              'Course ${provider.selectedProposalIndex + 1} of ${provider.proposals.length}',
                              style: const TextStyle(color: Colors.white70, fontSize: 12),
                            ),
                          ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),

                  // If multiple proposals, tabs/pills to switch
                  if (provider.proposals.length > 1) ...[
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: List.generate(provider.proposals.length, (index) {
                          final item = provider.proposals[index];
                          final isSelected = index == provider.selectedProposalIndex;
                          return Padding(
                            padding: const EdgeInsets.only(right: 8.0),
                            child: ChoiceChip(
                              label: Text('Course ${index + 1}: ${item.courseName}'),
                              selected: isSelected,
                              onSelected: (_) {
                                provider.selectProposal(index);
                                _syncControllersWithProposal(provider.proposals[index]);
                                setState(() {});
                              },
                              selectedColor: Colors.blueAccent,
                              backgroundColor: const Color(0xFF1E293B),
                              labelStyle: TextStyle(
                                color: isSelected ? Colors.white : Colors.grey.shade400,
                              ),
                            ),
                          );
                        }),
                      ),
                    ),
                    const SizedBox(height: 24),
                  ],

                  // Editable Form Fields
                  // 1. Course Name
                  const Text('Course Name', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white70)),
                  const SizedBox(height: 6),
                  TextField(
                    controller: _nameController,
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    onChanged: (val) => provider.updateCurrentProposal(courseName: val),
                    decoration: InputDecoration(
                      filled: true,
                      fillColor: const Color(0xFF0F172A),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                  ),
                  const SizedBox(height: 18),

                  // 2. Course Overview
                  const Text('Course Overview / Intended Learning Outcomes', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white70)),
                  const SizedBox(height: 6),
                  TextField(
                    controller: _overviewController,
                    maxLines: 3,
                    style: const TextStyle(color: Colors.white),
                    onChanged: (val) => provider.updateCurrentProposal(overview: val),
                    decoration: InputDecoration(
                      filled: true,
                      fillColor: const Color(0xFF0F172A),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                    ),
                  ),
                  const SizedBox(height: 18),

                  // Row: Duration, Level, Audience
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Duration
                      Expanded(
                        flex: 2,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Duration (Minutes)', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white70)),
                            const SizedBox(height: 6),
                            TextField(
                              controller: _durationController,
                              keyboardType: TextInputType.number,
                              style: const TextStyle(color: Colors.white),
                              onChanged: (val) {
                                final parsed = int.tryParse(val);
                                if (parsed != null) provider.updateCurrentProposal(durationMinutes: parsed);
                              },
                              decoration: InputDecoration(
                                prefixIcon: const Icon(Icons.timer_outlined, color: Colors.blueAccent),
                                filled: true,
                                fillColor: const Color(0xFF0F172A),
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 16),

                      // Level Dropdown
                      Expanded(
                        flex: 2,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Entry Level', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white70)),
                            const SizedBox(height: 6),
                            DropdownButtonFormField<String>(
                              value: _selectedLevel,
                              dropdownColor: const Color(0xFF1E293B),
                              style: const TextStyle(color: Colors.white),
                              items: const [
                                DropdownMenuItem(value: 'beginner', child: Text('Beginner / Fundamental')),
                                DropdownMenuItem(value: 'intermediate', child: Text('Intermediate')),
                                DropdownMenuItem(value: 'advanced', child: Text('Advanced')),
                              ],
                              onChanged: (val) {
                                if (val != null) {
                                  setState(() => _selectedLevel = val);
                                  provider.updateCurrentProposal(level: val);
                                }
                              },
                              decoration: InputDecoration(
                                filled: true,
                                fillColor: const Color(0xFF0F172A),
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 16),

                      // Audience
                      Expanded(
                        flex: 3,
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Target Audience', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white70)),
                            const SizedBox(height: 6),
                            TextField(
                              controller: _audienceController,
                              style: const TextStyle(color: Colors.white),
                              onChanged: (val) => provider.updateCurrentProposal(audience: val),
                              decoration: InputDecoration(
                                filled: true,
                                fillColor: const Color(0xFF0F172A),
                                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),

                  // Detected Topics Badges
                  if (proposal.topics.isNotEmpty) ...[
                    const Text('Detected Course Topics', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white70)),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: proposal.topics.map((t) {
                        return Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: Colors.blue.withOpacity(0.12),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: Colors.blueAccent.withOpacity(0.3)),
                          ),
                          child: Text(t, style: const TextStyle(color: Colors.lightBlueAccent, fontSize: 13)),
                        );
                      }).toList(),
                    ),
                    const SizedBox(height: 24),
                  ],

                  // Curated Reference Videos Preview
                  if (proposal.referenceVideos.isNotEmpty) ...[
                    const Text('Curated Supplementary Videos', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white70)),
                    const SizedBox(height: 8),
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: const Color(0xFF0F172A),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Column(
                        children: proposal.referenceVideos.map((vid) {
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4.0),
                            child: Row(
                              children: [
                                const Icon(Icons.play_circle_fill, color: Colors.redAccent, size: 20),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: Text(
                                    '${vid.title} (${vid.publisher})',
                                    style: const TextStyle(color: Colors.white, fontSize: 13),
                                  ),
                                ),
                              ],
                            ),
                          );
                        }).toList(),
                      ),
                    ),
                    const SizedBox(height: 28),
                  ],

                  // Action Buttons
                  Row(
                    children: [
                      OutlinedButton.icon(
                        onPressed: () => provider.setTab(AppViewTab.input),
                        icon: const Icon(Icons.arrow_back),
                        label: const Text('Cancel / Start Over'),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.grey.shade400,
                          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                        ),
                      ),
                      const Spacer(),
                      ElevatedButton.icon(
                        onPressed: provider.isLoading ? null : () => provider.approveAndBuildCurrentCourse(),
                        icon: const Icon(Icons.check_circle_outline, color: Colors.white),
                        label: const Text(
                          'Approve & Build Moodle Package',
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                        ),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.greenAccent.shade700,
                          padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 16),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
