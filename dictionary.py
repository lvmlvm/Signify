import question as qs


class TrieNode:
    def __init__(self, char):
        self.children = {}
        self.char = char
        self.is_end = False


class Trie:
    def __init__(self):
        self.topic = {}
        self.words = []

        topics = ['Bảng chữ cái', 'Chữ số', 'Ngày lễ']

        for topic in topics:
            for word in qs.subjects[topic]['content']:
                self.topic[word] = topic
                self.words.append(word)

        self.root = TrieNode('')
        self.build()

    def build(self):
        for word in self.words:
            self.insert(word)

    def insert(self, word):
        node = self.root

        for char in word:
            if char in node.children:
                node = node.children[char]

            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        node.is_end = True

    def get_child_words(self, cur_word: str):
        node = self.root

        for char in cur_word:
            if char in node.children:
                node = node.children[char]

        words = []

        def dfs(node):
            nonlocal words, cur_word

            if node.is_end:
                words.append(cur_word)

            for char in node.children:
                cur_word += char
                dfs(node.children[char])

            cur_word = cur_word[:-1]

        dfs(node)

        return words


if __name__ == '__main__':
    word = input()
    trie = Trie()
    print(trie.get_child_words(word))