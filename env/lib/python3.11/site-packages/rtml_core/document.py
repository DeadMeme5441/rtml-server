import os
import re

from rtml_core.tag import Tag


class Document:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.data = open(path).read()
        self.tags = []
        self.closing_errors = []
        self.opening_errors = []

        self.opening_tags()
        self.closing_tags()

        self.error_check()

        for tag in self.tags:
            tag.enclosing_pairs()

        self.total_tags = len(self.tags)
        self.total_errors = len(self.closing_errors) + len(self.opening_errors)

    def __dict__(self):
        return {
            "path": self.path,
            "name": self.name,
            "data": self.data,
            "tags": [tag.__dict__() for tag in self.tags],
            "total_tags": self.total_tags,
            "total_errors": self.total_errors,
            "closing_errors": [tag.__dict__() for tag in self.closing_errors],
            "opening_errors": [tag.__dict__() for tag in self.opening_errors],
        }

    def opening_tags(self):
        for match in re.finditer("<[^/].*?>", self.data):
            start_position = match.end()
            cleaned = match.group().strip("<>").strip(";").split(";")
            cleaned = [x.strip() for x in cleaned]
            for tag in cleaned:
                if tag not in [t.name for t in self.tags]:
                    self.tags.append(Tag(tag, start_position))
                else:
                    for t in self.tags:
                        if t.name == tag:
                            t.add_start_position(start_position)

        return self.tags

    def closing_tags(self):
        for match in re.finditer("</.*?>", self.data):
            end_position = match.start()
            cleaned = match.group().strip("</>").split(";")
            cleaned = [x.strip() for x in cleaned]
            tag_names = [tag.name for tag in self.tags]

            for tag in cleaned:
                if tag not in tag_names:
                    self.tags.append(Tag(tag))

                for t in self.tags:
                    if t.name == tag:
                        t.add_end_position(end_position)

    def error_check(self):
        for tag in self.tags:
            if len(tag.start_positions) > len(tag.end_positions):
                # print(
                #     f"Error: {tag.name} tag is not closed properly., opened at {[str(x) for x in tag.start_positions]}"
                # )
                self.tags.remove(tag)
                self.closing_errors.append(tag)
            elif len(tag.start_positions) < len(tag.end_positions):
                # print(
                #     f"Error: {tag.name} tag is not opened properly., closed at {[str(x) for x in tag.end_positions]}"
                # )
                self.tags.remove(tag)
                self.opening_errors.append(tag)
