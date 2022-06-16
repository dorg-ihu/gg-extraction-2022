import fitz
import re
from gm3.gm3.pparser import IssueParser

class PreParser:
    """
    
    """
    def __init__(self) -> None:
        pass


    def reorder_first_page(self, texts):
        """
        There are cases where "ΕΦΗΜΕΡΙΔΑ ΤΗΣ ΚΥΒΕΡΝΗΣΕΩΣ" doesn't appear in the beginning.
        This function detects such cases and reorders them in the beginning.
        """

        w = None
        if not re.search(r"ΕΦΗΜΕΡΙ(Σ|ΔΑ)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ", texts[0]):
            ind = 0
            for i, block in enumerate(texts):
                if re.search(r"ΕΦΗΜΕΡΙ(Σ|ΔΑ)\s+ΤΗΣ\s+ΚΥΒΕΡΝΗΣΕΩΣ", block):
                    ind = i
                    break

            w = texts[i:]+texts[:i]
        
        return w
    

    def fix_article_errors(self, doc):
        """
        There are cases where an article appears like "Άρθ ρο".
        The same happens in the next line and same index.
        """

        texts = doc.splitlines()

        for i, text in enumerate(texts):

            pattern = r'^Ά(\s*)ρ(\s*)θ(\s*)ρ(\s*)ο'
            
            q = re.search(pattern, text)
            if q:
                if not all(x == "" for x in q.groups()):
                    for j, item in enumerate(q.groups()):
                        if item:
                            ind = j+1
                            break
                    texts[i] = texts[i][:ind] + texts[i][ind+1:]
                    texts[i+1] = texts[i+1][:ind] + texts[i+1][ind+1:]
        
        doc = "\n".join(texts)
        
        return doc
        

    def pdf2text(self, fekpath, savefile=True):
        """
        Convert PDF file to TXT with some preprocessing
        """
        # Parse PDF file in blocks
        pages = []
        with fitz.open(fekpath,) as doc:
            for page in doc:
                text = page.get_text("blocks")
                pages.append(text)
        
        # Get text of each block and exclude signature information
        pages = [[item[4] for item in page if not re.search(r"(Digitally signed|Signature)", item[4])] for page in pages]

        # Fix problematic Δ representation. Even thought it seems the same, when converted to unicode has different value 
        pages = [[re.sub(r"∆", r"Δ", item) for item in page] for page in pages]

        # Reorder first page
        pages[0] = self.reorder_first_page(pages[0])
        # pages = [self.reorder_first_page(page) for page in pages]

        doc = "".join(block for page in pages for block in page)

        doc = self.fix_article_errors(doc)


        doc = doc.replace("-\n", "")
        doc = doc.replace("−\n", "")
        


        if savefile:
            savepath = re.sub(r".pdf$", ".txt", fekpath)
            with open(savepath, 'w', encoding='utf-8') as f:
                f.write(doc)
        
        return doc
    

class FekParser(IssueParser):
    """
    Reusing IssueParser from 3gm
    """
    def __init__(self, filename, stdin=False, toTxt=False):
        super().__init__(filename, stdin, toTxt)



