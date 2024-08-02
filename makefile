.PHONY: install create-namespace

install: create-namespace
	pip install -r requirements.txt
	@echo "Libraries installed successfully."

create-namespace:
	kubectl create namespace node1-namespace
	kubectl create namespace node2-namespace
	
	@echo "Namespace created successfully."
