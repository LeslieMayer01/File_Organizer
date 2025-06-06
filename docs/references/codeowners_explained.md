# 👥 CODEOWNERS File Explained

The `CODEOWNERS` file is a special configuration used by GitHub to automatically
assign reviewers to pull requests that affect specific files or directories.
It helps clarify ownership and responsibility across the codebase.

## 📑 Table of Contents

- [🔍 What is CODEOWNERS?](#-what-is-codeowners)
- [⚙️ How It Works](#️-how-it-works)
- [📁 File Location](#-file-location)
- [🧩 Syntax and Rules](#-syntax-and-rules)
- [👥 Our Project Ownership](#-our-project-ownership)
- [📄 Example Used](#-example-used)

---

## 🔍 What is CODEOWNERS?

It is a GitHub-supported configuration file that defines who owns what
part of the repository. Owners listed will automatically be requested
to review pull requests affecting their files.

---

## ⚙️ How It Works

When someone opens a pull request that modifies files:

- GitHub checks the `CODEOWNERS` file.
- If any matching pattern exists, the specified users or teams are requested
as reviewers.
- These reviewers help ensure the integrity and quality of changes.

---

## 📁 File Location

GitHub recognizes the `CODEOWNERS` file when placed in:

- `.github/CODEOWNERS`
- `docs/CODEOWNERS`
- Root of the repository: `CODEOWNERS`

We recommend placing it at the root level for simplicity.

---

## 🧩 Syntax and Rules

```plaintext
<file-or-directory-pattern> <@user1> <@user2> ...
```

- Patterns can include wildcards like `*` or `**`.
- Owners can be individual GitHub usernames or team names (e.g., `@org/team`).

---

## 👥 Our Project Ownership

In our case, both **Jorge (@jorduque16)** and **Leslie (@LeslieMayer01)**
are maintainers of the project. They co-own:

- All code and scripts
- All documentation
- Test coverage
- Project configuration

---

## 📄 Example Used

```plaintext
*                         @jorduque16 @LeslieMayer01
/docs/                    @jorduque16 @LeslieMayer01
/src/organizer/step5_create_electronic_index.py  @jorduque16 @LeslieMayer01
/src/organizer/11_Create_Index_File.py           @jorduque16 @LeslieMayer01
/tests/                   @jorduque16 @LeslieMayer01
Makefile                 @jorduque16 @LeslieMayer01
requirements.txt         @jorduque16 @LeslieMayer01
.pre-commit-config.yaml  @jorduque16 @LeslieMayer01
```

---

📌 **Tip:** If your repository is public, this configuration also helps
contributors know who to contact for specific parts of the code.

🔗 [Back to Main Index](../index.md)
