import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/course_generator_provider.dart';
import 'input_section.dart';
import 'review_gate_screen.dart';
import 'progress_screen.dart';
import 'downloads_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<CourseGeneratorProvider>();

    return Scaffold(
      backgroundColor: const Color(0xFF0B0F19),
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(70),
        child: Container(
          decoration: BoxDecoration(
            color: const Color(0xFF111827),
            border: Border(bottom: BorderSide(color: Colors.white.withOpacity(0.08))),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Row(
            children: [
              // Brand Logo & Title
              Container(
                height: 38,
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Image.asset(
                  'assets/fusionaix-logo.png',
                  height: 24,
                  fit: BoxFit.contain,
                  errorBuilder: (context, error, stackTrace) => const Icon(
                    Icons.auto_awesome,
                    color: Color(0xFF1E2B58),
                    size: 24,
                ),
              ),
              const SizedBox(width: 10),
              Container(
                height: 38,
                padding: const EdgeInsets.symmetric(horizontal: 14),
                decoration: BoxDecoration(
                  color: const Color(0xFF141414),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.white.withOpacity(0.12)),
                ),
                alignment: Alignment.center,
                child: const Text(
                  'Moodle Studio',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                    letterSpacing: -0.2,
                  ),
                ),
              ),
              const SizedBox(width: 24),

              // Navigation Tabs
              _buildNavButton(
                context,
                title: '1. Input Source',
                icon: Icons.edit_note,
                tab: AppViewTab.input,
                isActive: provider.currentTab == AppViewTab.input,
              ),
              const SizedBox(width: 8),
              _buildNavButton(
                context,
                title: '2. Review Gate',
                icon: Icons.verified,
                tab: AppViewTab.review,
                isActive: provider.currentTab == AppViewTab.review,
                badgeCount: provider.proposals.length > 1 ? provider.proposals.length : null,
              ),
              const SizedBox(width: 8),
              _buildNavButton(
                context,
                title: '3. Build & Package',
                icon: Icons.precision_manufacturing,
                tab: AppViewTab.progress,
                isActive: provider.currentTab == AppViewTab.progress,
              ),
              const SizedBox(width: 8),
              _buildNavButton(
                context,
                title: 'Course Library',
                icon: Icons.folder_zip,
                tab: AppViewTab.history,
                isActive: provider.currentTab == AppViewTab.history,
              ),

              const Spacer(),

              // Environment Status Badges
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: const Color(0xFF1F2937),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: Colors.white.withOpacity(0.06)),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 8,
                      height: 8,
                      decoration: const BoxDecoration(
                        color: Colors.greenAccent,
                        shape: BoxShape.circle,
                      ),
                    ),
                    const SizedBox(width: 8),
                    const Text(
                      'Local LLM: Ready',
                      style: TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      body: AnimatedSwitcher(
        duration: const Duration(milliseconds: 250),
        child: _buildCurrentScreen(provider.currentTab),
      ),
    );
  }

  Widget _buildCurrentScreen(AppViewTab tab) {
    switch (tab) {
      case AppViewTab.input:
        return const InputSection();
      case AppViewTab.review:
        return const ReviewGateScreen();
      case AppViewTab.progress:
        return const ProgressScreen();
      case AppViewTab.history:
        return const DownloadsScreen();
    }
  }

  Widget _buildNavButton(
    BuildContext context, {
    required String title,
    required IconData icon,
    required AppViewTab tab,
    required bool isActive,
    int? badgeCount,
  }) {
    final provider = context.read<CourseGeneratorProvider>();

    return InkWell(
      onTap: () => provider.setTab(tab),
      borderRadius: BorderRadius.circular(8),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          color: isActive ? Colors.blueAccent.withOpacity(0.18) : Colors.transparent,
          borderRadius: BorderRadius.circular(8),
          border: isActive
              ? Border.all(color: Colors.blueAccent.withOpacity(0.4))
              : null,
        ),
        child: Row(
          children: [
            Icon(
              icon,
              size: 18,
              color: isActive ? Colors.blueAccent : Colors.grey.shade400,
            ),
            const SizedBox(width: 8),
            Text(
              title,
              style: TextStyle(
                color: isActive ? Colors.white : Colors.grey.shade400,
                fontWeight: isActive ? FontWeight.bold : FontWeight.w500,
                fontSize: 13,
              ),
            ),
            if (badgeCount != null) ...[
              const SizedBox(width: 6),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: Colors.blueAccent,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Text(
                  '$badgeCount',
                  style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
