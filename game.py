#!/usr/bin/python

import sys, json

game = [{} for i in range(5)]

def create_answer(type,answer,question):
	out = {}
	out['type'] = type
	out['answer'] = answer
	out['question'] = question
	return out

game[0]['category'] = 'Category 1'
game[0]['level'] = []
game[0]['level'].append(create_answer('text','Answer 1','Question 1'))
game[0]['level'].append(create_answer('text','Answer 2','Question 2'))
game[0]['level'].append(create_answer('text','Answer 3','Question 3'))
game[0]['level'].append(create_answer('text','Answer 4','Question 4'))
game[0]['level'].append(create_answer('text','Answer 5','Question 5'))

game[1]['category'] = 'Category 2'
game[1]['level'] = []
game[1]['level'].append(create_answer('text','Answer 1','Question 1'))
game[1]['level'].append(create_answer('text','Answer 2','Question 2'))
game[1]['level'].append(create_answer('text','Answer 3','Question 3'))
game[1]['level'].append(create_answer('text','Answer 4','Question 4'))
game[1]['level'].append(create_answer('text','Answer 5','Question 5'))

game[2]['category'] = 'Category 3'
game[2]['level'] = []
game[2]['level'].append(create_answer('text','Answer 1','Question 1'))
game[2]['level'].append(create_answer('text','Answer 2','Question 2'))
game[2]['level'].append(create_answer('text','Answer 3','Question 3'))
game[2]['level'].append(create_answer('text','Answer 4','Question 4'))
game[2]['level'].append(create_answer('text','Answer 5','Question 5'))

game[3]['category'] = 'Category 4'
game[3]['level'] = []
game[3]['level'].append(create_answer('text','Answer 1','Question 1'))
game[3]['level'].append(create_answer('text','Answer 2','Question 2'))
game[3]['level'].append(create_answer('text','Answer 3','Question 3'))
game[3]['level'].append(create_answer('text','Answer 4','Question 4'))
game[3]['level'].append(create_answer('text','Answer 5','Question 5'))

game[4]['category'] = 'Category 5'
game[4]['level'] = []
game[4]['level'].append(create_answer('text','Answer 1','Question 1'))
game[4]['level'].append(create_answer('text','Answer 2','Question 2'))
game[4]['level'].append(create_answer('text','Answer 3','Question 3'))
game[4]['level'].append(create_answer('text','Answer 4','Question 4'))
game[4]['level'].append(create_answer('text','Answer 5','Question 5'))


json_out = json.dumps(game,sort_keys=True,indent=4)
print(json_out)
with open('test_game','w') as file:
	file.write(json_out)
