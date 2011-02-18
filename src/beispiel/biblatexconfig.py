from quotationtool.biblatex.configuration import BiblatexConfiguration

class BiblatexConfigurationBSP(BiblatexConfiguration):
    
    babel_languages = ('english', 'latin', 'french', 'german', 'ngerman')
    languages = ('ngerman',)
    default_language = 'ngerman'
    

config = BiblatexConfigurationBSP()


