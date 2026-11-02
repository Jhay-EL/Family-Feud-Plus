import 'package:flutter/material.dart';
import '../constants/game_colors.dart';

class GameTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
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
      tabBarTheme: const TabBarThemeData(
        labelColor: GameColors.textWhite,
        unselectedLabelColor: GameColors.textDark,
        indicatorSize: TabBarIndicatorSize.tab,
        labelStyle: TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
        unselectedLabelStyle: TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
        indicator: BoxDecoration(
          color: GameColors.primaryBlue,
          borderRadius: BorderRadius.vertical(top: Radius.circular(6)),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: GameColors.gameGreen,
          foregroundColor: GameColors.textWhite,
          elevation: 1,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(5)),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          textStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: GameColors.cardWhite,
        contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(5),
          borderSide: const BorderSide(color: GameColors.borderLight),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(5),
          borderSide: const BorderSide(color: GameColors.borderLight),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(5),
          borderSide: const BorderSide(color: GameColors.primaryBlue, width: 2),
        ),
      ),
    );
  }
}
