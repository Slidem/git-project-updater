class ProjectProcessorLinkChain:

    def __init__(self, root, projects):
        self.root = root

    def process_projects(self):
        link = self.root
        processed = self.projects
        while link:
            processed = link.process(processed)
            link = link.next
        return processed
