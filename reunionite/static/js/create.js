function addQuestion(question){
	new_question = document.createElement(div);
	question_title = document.createElement(input);
	question_title.setAttribute("type", "text");
	question_title.setAttribute("name", "question_" + question.id);
	question_list = document.createElement(ul);
	
	new_question.appendChild(question_title);
	new_question.appendChild(question_list);
	
	document.getElementById("poll").appendChild(new_question);
	
	return question_list;
}

function addOption(question, option){
	container = document.createElement(li);
	option = document.createElement(input);
	option.setAttribute("type", "text");
	option.setAttribute("name", "question_" + question.id);
	
	container.appendChild(option);
	question.appendChild(container);
}
