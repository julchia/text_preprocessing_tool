from typing import List, Dict, Union, Iterable, Generator, Callable

from src.core.management.managers import CorpusLazyManager
from src.core.processes.normalization.norm_utils import (
    punctuaction_handler, 
    lowercase_diacritic_handler
)


class Vocabulary:
    """
    """
    
    def __init__(
        self, 
        corpus: Union[List[str], str],
        corpus2sent: bool = False,
        text2idx: Dict[str, int] = None,
        add_unk: bool = True, 
        unk_text: str = "<<UNK>>",
        diacritic: bool = False,
        lower_case: bool = False,
        norm_punct: bool = False,
        corpus_iterator: Callable[[Union[List[str], str]], Iterable] = CorpusLazyManager
        
        ) -> None:
        """
        If 'corpus2sent' is False: variable 'text' is equivalent to 
        one unique token.
        If 'corpus2sent' is True: variable 'text' is equivalent to 
        entire unique sentence.
        
        """
        self._corpus_iterator = corpus_iterator
        
        self._corpus2sent = corpus2sent
        
        self._norm_punct = norm_punct
        self._lower_case = lower_case
        self._diacritic = diacritic
        
        if text2idx is None:
            text2idx = {}
        self._text2idx = text2idx

        self._idx2text = {
            idx: text
            for text, idx in self._text2idx.items()
        }
        
        self._add_unk = add_unk
                
        if unk_text is not None and not isinstance(unk_text, str):
            raise ValueError(
                "Invalid unk token object type. Expected str "
                f"but {type(unk_text)} was received"
            )
        
        self._unk_text = unk_text
        
        self.unk_idx = -1
                
        if unk_text is not None:
            self.unk_idx = self.add_text(unk_text)
        
        self.__init_vocab_from_iterable(
            self._corpus_iterator(corpus)
        )
    
    def __str__(self) -> str:
        return f"<Vocabulary object (size={len(self)})>"
    
    def __len__(self) -> int:
        return len(self._text2idx)
    
    def __iter__(self) -> Generator:
        for text in self._text2idx.keys():
            if self._corpus2sent:
                text = text.split()
            yield text

    def __init_vocab_from_iterable(
        self, 
        iterable: Iterable[List[str]]
    ) -> None:
        for text in iterable:
            self.add_text(text)

    def add_text(self, text: str) -> None:
        """
        """
        if self._lower_case or self._diacritic:
            text = lowercase_diacritic_handler(text=text)
        
        if self._norm_punct:
            text = punctuaction_handler(text=text, repl="")

        if text in self._text2idx:
            idx = self._text2idx[text]
        else:
            idx = len(self._text2idx)
            self._text2idx[text] = idx
            self._idx2text[idx] = text
    
    def get_idx_by_text(self, text: str) -> int:
        """
        """
        if self._add_unk:
            return self._text2idx.get(text, self.unk_idx)
        else:
            return self._text2idx[text]
        
    def get_text_by_index(self, index: int) -> str:
        """
        """
        if index not in self._idx2text:
            raise KeyError(f"The index {index} is not in the Vocabulary")
        return self._idx2text[index]

