import 'package:flutter/material.dart';

/// Central design tokens and color palette for Family Feud+
class GameColors {
  // Brand & Navigation
  static const Color primaryBlue = Color(0xFF004AAD);
  static const Color primaryBlueDark = Color(0xFF002D6B);
  
  // Game Actions
  static const Color gameGreen = Color(0xFF008F4A);
  static const Color gameGreenHover = Color(0xFF00A65A);
  static const Color gameGreenPressed = Color(0xFF006F3A);
  
  // Alerts & Strikes
  static const Color strikeRed = Color(0xFFB80000);
  static const Color strikeRedHover = Color(0xFFCC0000);
  static const Color strikeRedPressed = Color(0xFF990000);
  
  // Accents & Highlights
  static const Color goldAmber = Color(0xFFF9B451);
  static const Color cautionOrange = Color(0xFFEA7620);
  
  // Surfaces & Backgrounds
  static const Color surfaceLight = Color(0xFFF9F9F9);
  static const Color cardWhite = Color(0xFFFFFFFF);
  static const Color borderLight = Color(0xFFDCDCDC);
  static const Color disabledBg = Color(0xFFDCDCDC);
  
  // Text Colors
  static const Color textDark = Color(0xFF222222);
  static const Color textMuted = Color(0xFF777777);
  static const Color textWhite = Color(0xFFFFFFFF);
}

/// Global Theme styling for Family Feud+
class GameTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      brightness: Brightness.light,
      primaryColor: GameColors.primaryBlue,
      scaffoldBackgroundColor: GameColors.surfaceLight,
      colorScheme: const ColorScheme.light(
        primary: GameColors.primaryBlue,
        secondary: GameColors.gameGreen,
        error: GameColors.strikeRed,
        surface: GameColors.surfaceLight,
      ),
      fontFamily: 'Segoe UI',
      tabBarTheme: TabBarTheme(
        labelColor: GameColors.textWhite,
        unselectedLabelColor: GameColors.textDark,
        indicatorSize: TabBarIndicatorSize.tab,
        indicator: BoxDecoration(
          color: GameColors.primaryBlue,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(6)),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: GameColors.gameGreen,
          foregroundColor: GameColors.textWhite,
          elevation: 1,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          textStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
        ),
      ),
    );
  }
}
