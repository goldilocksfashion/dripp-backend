git filter-repo --email-callback '
    if commit.author_email == b"anirudhvyas@Anirudhs-MacBook-Pro.local":
        commit.author_email = b"ricky.nj@gmail.com"
        return commit
    if commit.committer_email == b"anirudhvyas@Anirudhs-MacBook-Pro.local":
        commit.committer_email = b"ricky.nj@gmail.com"
        return commit
'
