# 📌 **Regex Libraries Used in Software & Programming Languages**

## **🖥️ Text Editors & IDEs**
- **Notepad++** → [Boost.Regex](https://www.boost.org/doc/libs/1_81_0/libs/regex/doc/html/index.html) (C++ Boost library)
- **Visual Studio Code (VS Code)** → [ECMAScript RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)

- **Sublime Text** → [Oniguruma](https://github.com/kkos/oniguruma) (same as Ruby’s regex engine)
- **Atom** → [Oniguruma](https://github.com/kkos/oniguruma)
- **Vim** → Custom regex engine (inspired by POSIX but with Vim-specific syntax)
- **Emacs** → Custom regex engine (similar to POSIX but slightly different syntax)
- **Eclipse** → Java’s [`java.util.regex`](https://docs.oracle.com/javase/8/docs/api/java/util/regex/package-summary.html)
- **IntelliJ IDEA / PyCharm** → Java’s [`java.util.regex`](https://docs.oracle.com/javase/8/docs/api/java/util/regex/package-summary.html)

## **📄 Word Processors**
- **Microsoft Word** → Custom wildcard pattern matching (not full regex)
- **LibreOffice Writer** → [ICU](https://icu.unicode.org/) (International Components for Unicode)
- **Google Docs** → [Re2](https://github.com/google/re2) (Google’s regex engine)

## **💻 Command Line & Shells**
- **grep (GNU/Linux)** → POSIX Extended Regular Expressions (ERE)
- **sed / awk** → POSIX Basic/Extended Regular Expressions (BRE/ERE)
- **PowerShell** → [.NET `System.Text.RegularExpressions`](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions) (Perl-compatible)

## **🗄️ Databases**
- **MySQL** → [ICU Regex Engine](https://icu.unicode.org/) (from MySQL 8.0+)
- **PostgreSQL** → Tcl's regex engine (based on Spencer library)
- **MongoDB** → [PCRE](https://www.pcre.org/) (Perl-Compatible Regular Expressions)
- **Oracle SQL** → POSIX ERE

## **🌐 Web Browsers & JavaScript Engines**
- **Chrome / V8** → [ECMAScript RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)
- **Firefox / SpiderMonkey** → [ECMAScript RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)
- **Edge / Chromium** → [ECMAScript RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)
- **Safari / WebKit** → [ECMAScript RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)

## **🔧 Miscellaneous Software**
- **Wireshark** → [PCRE](https://www.pcre.org/) (Perl-Compatible Regular Expressions)
- **Adobe Photoshop (Find & Replace)** → Custom (not full regex support)
- **AutoHotkey** → [PCRE](https://www.pcre.org/)
- **R (`stringr`, base R)** → ICU, TRE, and PCRE depending on function

---

# **📜 Regex Libraries in Programming Languages**

## **🐍 Python**
- **`re`** (built-in)
- **[`regex`](https://pypi.org/project/regex/)** (third-party, enhanced version of `re`)

## **☕ Java**
- **[`java.util.regex`](https://docs.oracle.com/javase/8/docs/api/java/util/regex/package-summary.html)** (built-in)

## **⚙️ C# (.NET)**
- **[`System.Text.RegularExpressions`](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions)**

## **🟢 JavaScript**
- **[`RegExp`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp)** (ECMAScript built-in)

## **🐹 Go**
- **[`regexp`](https://pkg.go.dev/regexp)** (built-in)

## **🐘 PHP**
- **[`preg_*`](https://www.php.net/manual/en/ref.pcre.php)** (PCRE-based functions)

## **🐪 Perl**
- **PCRE (Perl-Compatible Regular Expressions)** (built-in)

## **🔵 R**
- **[`stringr`](https://cran.r-project.org/web/packages/stringr/index.html) (ICU, TRE, and PCRE depending on function)**

## **🐧 Linux CLI Tools**
- **`grep`, `sed`, `awk`** → POSIX BRE/ERE

## **📝 Key Takeaways**
- **Most modern software** uses **PCRE** (Perl-Compatible Regular Expressions) or **ICU**.
- **JavaScript-based apps** (VS Code, web browsers) rely on **ECMAScript regex**.
- **Older or specialized software** (like Notepad++) might use **Boost.Regex** or **custom engines**.

