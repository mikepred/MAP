import subprocess
import re
import os

# Use the current working directory as the repository path
REPO_PATH = "."

def get_local_branch_names():
    """Fetches all local branch names from the Git repository."""
    try:
        result = subprocess.run(
            ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads"],
            capture_output=True, text=True, check=True, cwd=REPO_PATH, encoding='utf-8'
        )
        branches = result.stdout.strip().split('\n')
        return set(b for b in branches if b) # Filter out empty strings if any
    except subprocess.CalledProcessError as e:
        print(f"Error getting local branch names: {e.stderr}")
        return set()
    except FileNotFoundError:
        print("Error: git command not found. Is Git installed and in your PATH?")
        return set()

def get_git_log_data():
    """
    Fetches Git log data: SHA, parent SHAs, and ref names for all commits,
    ordered chronologically (oldest first).
    """
    try:
        git_log_command = [
            "git", "log", "--all",
            "--pretty=format:%H|%P|%D", # Hash | Parent Hashes | Refs
            "--date-order", "--reverse" # Oldest first
        ]
        result = subprocess.run(
            git_log_command, capture_output=True, text=True, check=True, cwd=REPO_PATH, encoding='utf-8'
        )
        
        commits_data = []
        if not result.stdout.strip():
            return [] # No commits found

        for line in result.stdout.strip().split('\n'):
            parts = line.split('|', 2)
            sha = parts[0]
            parents = parts[1].split() if parts[1] else []
            refs_str = parts[2] if len(parts) > 2 else ""
            commits_data.append((sha, parents, refs_str))
        return commits_data
    except subprocess.CalledProcessError as e:
        print(f"Error getting git log: {e.stderr}")
        return []
    except FileNotFoundError:
        print("Error: git command not found. Is Git installed and in your PATH?")
        return []

def parse_commit_refs_for_local_branches(refs_str, all_local_branches_set):
    """
    Parses the ref string (%D from git log) for a commit and returns
    a set of local branch names that point to this commit.
    """
    commit_local_branches = set()
    if not refs_str.strip():
        return commit_local_branches

    refs_to_parse = refs_str
    # Remove surrounding parentheses if git log adds them (e.g., "(HEAD -> main, origin/main)")
    if refs_to_parse.startswith('(') and refs_to_parse.endswith(')'):
        refs_to_parse = refs_to_parse[1:-1]

    potential_refs = [p.strip() for p in refs_to_parse.split(',')]
    for ref in potential_refs:
        if ref.startswith("HEAD -> "):
            # Extract the branch name pointed to by HEAD
            branch_name_pointed_by_head = ref.split("HEAD -> ", 1)[1]
            # If HEAD points to a remote branch (e.g., origin/main),
            # check if its local counterpart exists.
            if branch_name_pointed_by_head.startswith("origin/"):
                local_equivalent = branch_name_pointed_by_head.replace("origin/", "", 1)
                if local_equivalent in all_local_branches_set:
                    commit_local_branches.add(local_equivalent)
            elif branch_name_pointed_by_head in all_local_branches_set:
                commit_local_branches.add(branch_name_pointed_by_head)
        elif ref in all_local_branches_set: # Direct local branch ref
            commit_local_branches.add(ref)
            
    return commit_local_branches

def generate_mermaid_code(commits_data, all_local_branches_set):
    """
    Generates Mermaid gitGraph syntax from commit data.
    Focuses on local branches and their connections.
    """
    if not commits_data:
        return "gitGraph LR;\n  commit id:\"No Commits Found\";"

    mermaid_lines = ["gitGraph LR;"] # Left-to-Right layout

    # Determine the primary line of development (e.g., main or master)
    # This will be the first branch checked out in Mermaid.
    main_line_branch = None
    if "main" in all_local_branches_set:
        main_line_branch = "main"
    elif "master" in all_local_branches_set:
        main_line_branch = "master"
    elif all_local_branches_set: # If main/master not found, pick one alphabetically
        main_line_branch = sorted(list(all_local_branches_set))[0]
    else: # No local branches found at all, but commits exist (e.g. detached HEAD)
          # Try to infer from HEAD in the first commit with refs
        for _, _, rs_init in commits_data:
            if "HEAD -> " in rs_init:
                potential_head_target = rs_init.split("HEAD -> ")[1].split(',')[0].strip()
                main_line_branch = potential_head_target.replace("origin/", "") # Use local part if remote
                break
        if not main_line_branch:
            main_line_branch = "start" # A generic name if no branches or HEAD found

    current_mermaid_branch = main_line_branch
    mermaid_lines.append(f"  checkout {current_mermaid_branch}")
    created_mermaid_branches = {current_mermaid_branch}
    
    # Map commit SHAs to the Mermaid branch they were primarily drawn on
    # This helps in identifying the source branch for merges.
    commit_sha_to_mermaid_branch = {}

    for sha, parents, refs_str in commits_data:
        commit_sha_short = sha[:7]
        
        # Identify local branches pointing directly to this commit
        branches_on_this_commit = parse_commit_refs_for_local_branches(refs_str, all_local_branches_set)

        # Determine the target branch for this commit in Mermaid
        # Priority: 1. A branch already created in Mermaid if this commit is on it.
        #           2. The main_line_branch if this commit is on it.
        #           3. Any other local branch on this commit.
        #           4. Default to current_mermaid_branch if no specific branch ref.
        
        target_branch_for_drawing = current_mermaid_branch # Default
        
        if branches_on_this_commit:
            if current_mermaid_branch in branches_on_this_commit:
                target_branch_for_drawing = current_mermaid_branch
            elif main_line_branch in branches_on_this_commit:
                target_branch_for_drawing = main_line_branch
            else: # Pick one from the branches on this commit
                target_branch_for_drawing = sorted(list(branches_on_this_commit))[0]
        
        # Switch branch in Mermaid if necessary
        if target_branch_for_drawing != current_mermaid_branch:
            if target_branch_for_drawing not in created_mermaid_branches:
                mermaid_lines.append(f"  branch {target_branch_for_drawing}")
                created_mermaid_branches.add(target_branch_for_drawing)
            mermaid_lines.append(f"  checkout {target_branch_for_drawing}")
            current_mermaid_branch = target_branch_for_drawing
        
        commit_sha_to_mermaid_branch[sha] = current_mermaid_branch

        # Add commit or merge command
        if len(parents) > 1: # Merge commit
            # Identify the branch that was merged into the current_mermaid_branch.
            # This is typically the parent that was NOT on the current_mermaid_branch's line.
            merged_from_branch = None
            for p_sha in parents:
                parent_mermaid_branch = commit_sha_to_mermaid_branch.get(p_sha)
                if parent_mermaid_branch and parent_mermaid_branch != current_mermaid_branch:
                    merged_from_branch = parent_mermaid_branch
                    break 
            
            if merged_from_branch:
                mermaid_lines.append(f"  merge {merged_from_branch} id:\"{commit_sha_short}\"")
            else:
                # Fallback if source branch is unclear (e.g., octopus merge or complex history)
                mermaid_lines.append(f"  commit id:\"{commit_sha_short}\" type:MERGE")
        else: # Regular commit or initial commit
            mermaid_lines.append(f"  commit id:\"{commit_sha_short}\"")
            
    return "\n".join(mermaid_lines)

def main():
    """Main function to generate and print the Mermaid graph for Git branches."""
    print("Attempting to generate Git branch visualization as Mermaid code...")
    
    local_branches = get_local_branch_names()
    if not local_branches:
        # Handle case where git might not be available or no local branches
        # get_git_log_data might still work if commits exist (e.g. detached HEAD)
        print("Info: No local branches found or git command failed for branches.")
        # We can proceed, generate_mermaid_code will try to adapt.

    log_data = get_git_log_data()

    if not log_data and not local_branches: # Truly empty or inaccessible repo
        print("gitGraph LR;\n  commit id:\"No Git data found (empty repository or Git error).\";")
        return
    
    # If log_data is empty but local_branches exist, it's an odd state (branches exist but no commits in log --all?)
    # This shouldn't happen in a normal repo. get_git_log_data() handles empty log.

    mermaid_script = generate_mermaid_code(log_data, local_branches)
    
    output_filename = "branch_visualization.mermaid.txt"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(mermaid_script)
        print(f"\nMermaid code successfully saved to: {output_filename}")
        print("You can copy the content of this file into a Mermaid renderer (e.g., https://mermaid.live).")
    except IOError as e:
        print(f"Error saving Mermaid code to file: {e}")
        # Fallback to printing to console if file write fails
        print("\n--- Mermaid GitGraph Code (Fallback) ---")
        print(mermaid_script)
        print("--- End of Mermaid Code (Fallback) ---\n")

if __name__ == "__main__":
    main()
