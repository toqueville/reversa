# Platform Detection

Heuristics that `reversa-screen-translator` uses to classify the legacy source platform from the contents of `_reversa_sdd/inventory.md` and source code. Use together with `references/adapter-pairs.md` to choose the adapter.

The confidence scale applied per classification:

- 🟢 **CONFIRMED**: at least one strong signature (header, namespace, unique marker) is present.
- 🟡 **INFERRED**: extension and general pattern match, but there is no unique signature.
- 🔴 **GAP**: source code artifact absent; classifies only from `inventory.md`.
- ⚠️ **AMBIGUOUS**: two plausible platforms tied (e.g.: classic ASP vs ASP.NET WebForms in old projects).

## Signature table

| Source slug | Typical extension | Strong signature | Weak signature |
|---|---|---|---|
| `cobol-ansi-tui` | `.cob`, `.cbl`, `.cpy` | `PROCEDURE DIVISION.` + `DISPLAY`/`ACCEPT` + `\x1B[` sequences, box-drawing Unicode (`╔ ╗ ┌ ┐`) | only `PROCEDURE DIVISION` (no ANSI = batch COBOL) |
| `cobol-screen-section` | `.cob`, `.cbl` | `SCREEN SECTION` + attributes `LINE`, `COLUMN`, `FOREGROUND-COLOR` | `SCREEN SECTION` without details |
| `ncurses-c` | `.c`, `.h` | `#include <ncurses.h>` or `<curses.h>` + `WINDOW *`, `wprintw`, `mvwaddstr` | `printf` + `\033[` (artisanal TUI) |
| `delphi-vcl` | `.pas`, `.dfm`, `.dpr` | `unit `, `interface`, `TForm`, `TPanel`, `TButton` in `.dfm` | `.pas` only without `.dfm` (likely CLI) |
| `delphi-firemonkey` | `.pas`, `.fmx` | `TForm` in `.fmx` file (FireMonkey) | only `.pas` |
| `vb6` | `.frm`, `.bas`, `.cls`, `.vbp` | `VERSION 5.00` in header, `Begin VB.Form`, `Begin VB.CommandButton` | `.bas` only (module without UI) |
| `vbnet-winforms` | `.vb` + `Designer.vb` | `Inherits System.Windows.Forms.Form` | only `Module ... Sub Main` (CLI) |
| `csharp-winforms` | `.cs`, `.designer.cs` | `using System.Windows.Forms;` + `partial class ... : Form` | only `using System;` |
| `csharp-wpf` | `.xaml`, `.cs` | `xmlns="http://schemas.microsoft.com/winfx/..."` + `<Window>`, `<Grid>` | only `.cs` without `.xaml` |
| `win32-mfc` | `.cpp`, `.h`, `.rc` | `BEGIN_MESSAGE_MAP`, `CDialog`, `WinMain`, `IDD_*` in `.rc` | standalone `WinMain` |
| `win32-raw` | `.cpp`, `.h` | `WinMain` + `RegisterClass`, `CreateWindow`, `WM_*` messages | only `WinMain` |
| `asp-classic` | `.asp`, `.inc` | `<%@ Language=VBScript %>` or `<%@ Language=JScript %>` + `Response.Write` | `.asp` without `<%@` |
| `aspnet-webforms` | `.aspx`, `.aspx.cs`, `.aspx.vb` | `<%@ Page Language="C#"`, `runat="server"`, `<asp:` controls | simple `.aspx` only |
| `jsp` | `.jsp`, `.jspf` | `<%@ page language="java" %>`, `<jsp:`, `<%! %>` | `.jsp` with only HTML |
| `php-server-rendered` | `.php` | `<?php ... ?>` + inline HTML + `mysql_*` or `mysqli_*` | only `.php` in `api/` folder (likely REST API, not UI) |
| `html-legacy-jquery` | `.html`, `.htm`, `.js` | `jQuery`/`$.ajax` + server-side form submits, no SPA framework | static HTML (no dynamic JS) |
| `android-xml-java` | `res/layout/*.xml`, `*.java` | `<LinearLayout>`/`<RelativeLayout>`/`<ConstraintLayout>` + `Activity extends`, `setContentView(R.layout...)` | only Java without `res/layout/` |
| `android-xml-kotlin` | `res/layout/*.xml`, `*.kt` | same as above + `Activity()` Kotlin + `setContentView(R.layout...)` | only Kotlin without `res/layout/` |
| `android-compose` | `*.kt` | `@Composable`, `setContent { ... }` | without `setContent` |
| `ios-xib-objc` | `.xib`, `.m`, `.h`, `.storyboard` | `UIViewController` + `*.xib` or `*.storyboard` referenced | only `*.m` without XIB |
| `ios-xib-swift` | `.xib`, `.swift`, `.storyboard` | `UIViewController` Swift + XIB/Storyboard | only `*.swift` without XIB |
| `ios-swiftui` | `*.swift` | `View` + `var body: some View`, `App` lifecycle | without `var body` |
| `flutter` | `*.dart`, `pubspec.yaml` | `import 'package:flutter/material.dart'` + `StatelessWidget`/`StatefulWidget` | without `material.dart` |
| `react-class` | `*.jsx`, `*.tsx` | `class ... extends React.Component` + `render()` | only `*.tsx` (likely modern) |
| `react-hooks` | `*.jsx`, `*.tsx` | `function ... ({...}) { return <...>; }` + `useState`, `useEffect` | (not legacy, is target) |

## Additional indicators

- **Directory structure**:
  - `forms/`, `Forms/` → Delphi, VB6, .NET WinForms.
  - `views/`, `templates/` → MVC server-side (ASP, JSP, PHP).
  - `app/src/main/res/layout/` → Android.
  - `Storyboard.storyboard` or `*.xib` at root → legacy iOS.
  - `Pages/` in Razor project → ASP.NET.
- **Build files**:
  - `*.dpr` (Delphi), `*.vbp` (VB6), `*.csproj` (.NET), `pom.xml`/`build.gradle` (Java/Android), `Podfile` (iOS), `pubspec.yaml` (Flutter).
- **Version strings in comments or headers**: VB6 marks `VERSION 5.00`; Delphi 7 marks `{$OBJECT}`; .NET with `<TargetFramework>net48</TargetFramework>` indicates legacy WinForms.

## When two platforms are tied

- **Classic ASP vs ASP.NET WebForms**: `.asp` files without `.aspx` → classic. `.aspx` + `.asp` in the same project → migrating project, mark ⚠️ AMBIGUOUS and ask.
- **VB6 vs VB.NET**: `.frm` + `.vbp` → VB6. `.vb` + `.designer.vb` + `.vbproj` → VB.NET WinForms.
- **Delphi VCL vs FireMonkey**: `.dfm` → VCL. `.fmx` → FireMonkey. Both in the project → mark ⚠️ AMBIGUOUS.
- **Android Java vs Kotlin**: `.java` + `.kt` in the same project → project in migration; classify per individual file.
- **iOS Storyboard vs XIB**: both supported; treat as one class (`ios-xib-*`). Difference goes in capture detail.

## When nothing matches

Record `EC-01` (unknown source platform) and offer the user a "raw" template where they describe the screen in structured prose, with mandatory sections:

- Identity.
- Layout in ASCII art or screenshot.
- List of fields / components.
- Literal messages / labels.
- Events and transitions.
- Validations.

The agent then generates `target_screens.md` with `spec.kind: raw-prose` and marks in `screen_deviation_log.md` that the screen did not go through the adapter.
