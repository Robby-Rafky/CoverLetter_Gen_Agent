Enter a bunch of details, and paste a job posting and this will generate a cover letter tailored
to the position based on your skillset and experiences.

Can be compatible with any model that works with langchain to have data exposed to model for
contextual generation.

To use this app:
Create a .env file with your API key assigned to "TOGETHER_API_KEY" and place it within the config folder.
```bash
git clone https://github.com/Robby-Rafky/CoverLetter_Gen_Agent.git

cd CoverLetter_Gen_Agent

python3 -m venv venv

# LINUX/MAC
source venv/bin/activate

# WINDOWS
venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

This application utilises together.ai to connect to a Llama-3.3 model (free version), so it might 
not be the most stable.
Model rate limit of 6 requests/min

#
Each section can be filled with information to assist the agent in fully personalising 
the coverletter to your skillset and experience.
<p align="center">
  <img src="https://github.com/user-attachments/assets/ac5a5b92-46e9-48de-982d-90850431c07e" alt="image" />
</p>

# 
The fields can be editied and are saved when the app is closed.
<p align="center">
  <img src="https://github.com/user-attachments/assets/f49e17fc-ddb5-42d5-8993-8f8f940a5b78" alt="image" />
</p>

# 
Additional entries can be added or deleted.
<p align="center">
  <img src="https://github.com/user-attachments/assets/3622d02e-88cc-4b00-a8a1-b050e8a53f47" alt="image" />
</p>

# 
The model takes an input of a job description, either manually written or simply copy and 
paste the full description.
<p align="center">
  <img src="https://github.com/user-attachments/assets/d249aad5-3b4c-478a-976e-2adc4acf0388" alt="image" />
</p>

#
The model will attempt to generate a cover letter tailored to the job description and 
personalised by the stored data.
<p align="center">
  <img src="https://github.com/user-attachments/assets/f3c81041-9b58-456c-8c11-a94b02328151" alt="image" />
</p>

#
The resultant cover letter can be copied to clipboard or saved locally.
<p align="center">
  <img src="https://github.com/user-attachments/assets/2fec71b1-3ada-4ea3-b685-06235e37cc5e" alt="image" />
</p>

# 
Parameters can be changed in the config folder such as the model & api base (if you'd like to use a better model)
The system prompt can also be changed if you'd like to generate other things based on the data stored and
exposed to the model via this app.
<p align="center">
  <img src="https://github.com/user-attachments/assets/d8c587d5-3a7c-4d6d-868d-6aae2eaa49d3" alt="image" />
</p>
