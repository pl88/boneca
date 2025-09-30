import shutil
from git import Repo

class Git:
    def __init__(self, id, project, revision):
        self.path = "/tmp/git_%s_%s_%s" %(str(project), str(revision), str(id))
        self.repo = None

    def clone(self, url, revision):
        try:
            self.repo = Repo.clone_from(url, self.path)
            self.repo.git.checkout("%s" %(revision))
            return True
        except Exception as e:
            print("Git failed: %s" %(str(e)))
            return False

    def bare(self, url):
        try:
            self.repo = Repo.clone_from(url, self.path, bare=True)
            return True
        except Exception as e:
            print("Git failed: %s" %(str(e)))
            return False
    
    def clean(self):
        shutil.rmtree(self.path)
        return True

    def getPath(self):
        return self.path

    def getRevision(self):
        return self.repo.head.commit.hexsha

    def getMessageFromRevision(self, revision):
        try:
            return self.repo.commit(revision).message
        except Exception as e:
            print("Git failed: %s" %(str(e)))
            return None

    def getMessage(self):
        return self.repo.head.commit.message

    def getCommitRange(self, revA, revB):
        return self.repo.iter_commits("%s..%s" %(str(revA), str(revB)))

    def getMessageRange(self, revA, revB):
        return map(lambda c: c.message, self.repo.iter_commits("%s..%s" %(str(revA), str(revB))))
