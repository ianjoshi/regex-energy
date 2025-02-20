# 📌 **Regex Libraries Used in Software & Programming Languages**

## **🖥️ Text Editors & IDEs**
- **Notepad++** → [Boost.Regex](https://www.boost.org/doc/libs/1_81_0/libs/regex/doc/html/index.html) (C++ Boost library)
- **Visual Studio Code (VS Code)** → [Javascript RegExp](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)

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


---

---


# 📌 Comparing Regex Engine Performance in Python

## 1. ✅ Regex Engines You Can Use in Python

### a) **RE2 (Google’s RE2)**
- Install with [`pyre2`](https://pypi.org/project/re2/).
- Optimized for speed and prevents catastrophic backtracking.

### b) **PCRE (Perl-Compatible Regular Expressions)**
- Python bindings available via [`pcre`](https://pypi.org/project/pcre/).
- More powerful than Python’s built-in `re` module.

### c) **Oniguruma (Used by Ruby, Sublime, Atom)**
- Python bindings: [`onigmo`](https://github.com/kkos/oniguruma) or `pyonig`.
- Supports complex regex features like named groups.

### d) **ICU (International Components for Unicode)**
- Python wrapper available: [`PyICU`](https://pypi.org/project/PyICU/).
- Often used in LibreOffice, MySQL 8+, and R.

### e) **Boost.Regex**
- No direct Python wrapper, but can be accessed via:
  - C++ bindings (`ctypes`, `pybind11`).
  - Custom-built Boost.Regex C++ wrapper.

---

## 2. ⚠️ Engines With Indirect or Tricky Python Access

### a) **Java’s `java.util.regex`**
- Can’t be imported in Python directly.
- Workarounds:
  - Run Java regex via [`subprocess`](https://docs.python.org/3/library/subprocess.html).
  - Use [`JPype`](https://pypi.org/project/JPype1/) to call Java from Python.

### b) **.NET `System.Text.RegularExpressions` (PowerShell)**
- No direct Python access.
- Workarounds:
  - Use **IronPython** (Python on .NET).
  - Run regex via PowerShell and capture output in Python.

### c) **POSIX BRE/ERE (`grep`, `sed`, `awk`)**
- Not directly available in Python.
- Workaround:
  - Execute shell commands via `subprocess.run(["grep", ...])`.

### d) **Vim / Emacs / Microsoft Word / Adobe Photoshop**
- No native Python support.
- These use **custom regex engines** tied to their respective software.

---

## 3. 🐍 Engines Already in Python

### a) **`re` (Built-in Python Module)**
- Standard regex engine in Python.
- Good for most cases but lacks advanced PCRE features.

### b) **`regex` (Third-party Module)**
- Enhanced version of `re` with additional features.
- Install with:  
  ```bash
  pip install regex
