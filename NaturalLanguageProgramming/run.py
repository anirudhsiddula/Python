from TextProcessor import TextProcessor


# pdtabulate=lambda df:tabulate(df,headers='keys',tablefmt='psql')
# print(pdtabulate(tp.pos_tag()))

raw_list ="          Jack and jill have made a delicious,       dish.Then they started to play some12 game! and jill has attahacd# [a] photo frame to the straight9 wall and swung on sea-saw. She was very happy. After the game, they both went to central London to enjoy some fast food."
print("raw input: {}".format(raw_list))
print('\n\n\n')

tp = TextProcessor(raw_list)

#Cleaning:
tp.clean()

print("before Spell Correction: {}".format(tp.text))
print('\n\n\n')
# tp.spell_correct()         #RegularExp

tp.spell_correct1()         #TextBlob
# tp.spell_correct2()         #Dropped approch using POS

print("After Spell Correction: {}".format(tp.text))
print('\n\n\n')

#Tokenization
tp.tokeni('wordpunct_tokenize')
print('tokens: {}'.format(tp.tokens))
print('\n\n\n')

#Parts of Speech Tagging
tp.pos()
print('Parts of Speech Tagged Input: {}'.format(tp.pos_out))
print('\n\n\n')

#Name Entity Recognition
tp.NameEntityRecognition()
print('Entity Tagged output: {}'.format(tp.entities))
print('\n\n\n')


#N-grams
tp.ngrams()
# tp.ngrams(5)
print('N-grams : {}'.format(tp.n_grams))
