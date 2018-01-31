# -*- coding: utf-8 -*-
import preprocessor as p
print p.clean('Preprocessor is #awesome 👍 https://github.com/s/preprocessor')

print p.tokenize('Preprocessor is #awesome 👍 https://github.com/s/preprocessor')

print p.parse('Preprocessor is #awesome 👍 https://github.com/s/preprocessor').hashtags

l=p.parse('Preprocessor is #awesome 👍 https://github.com/s/preprocessor').hashtags

print l[0].match


