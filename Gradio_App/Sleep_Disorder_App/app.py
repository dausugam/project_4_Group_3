import tensorflow as tf
import gradio as gr
import numpy as np

# Load the trained model
model = tf.keras.models.load_model('sleep_disorder_model.h5')

# Define the prediction function
def predict_sleep_disorder(gender, age, sleep_duration, quality_of_sleep, physical_activity_level, stress_level, heart_rate, daily_steps, systolic, diastolic, occupation, bmi_category):
    # Gender encoding
    gender_male = 1 if gender == "Male" else 0
    
    # Occupation encoding
    occupation_dict = {
        "Doctor": 0, "Engineer": 1, "Lawyer": 2, "Manager": 3,
        "Nurse": 4, "SalesRepresentative": 5, "Salesperson": 6, 
        "Scientist": 7, "SoftwareEngineer": 8, "Teacher": 9
    }
    occupation_encoded = [0] * 10  # Initialize a list of 10 zeros
    if occupation in occupation_dict:
        occupation_encoded[occupation_dict[occupation]] = 1  # Set the correct occupation to 1
    
    # BMI Category encoding
    bmi_dict = {
        "NormalWeight": 0, 
        "Obese": 1, 
        "Overweight": 2
    }
    bmi_encoded = [0, 0, 0]  # Initialize a list of 3 zeros
    if bmi_category in bmi_dict:
        bmi_encoded[bmi_dict[bmi_category]] = 1  # Set the correct BMI category to 1

    # Combine all inputs into a single array
    input_data = np.array([[
        age, sleep_duration, quality_of_sleep, physical_activity_level, 
        stress_level, heart_rate, daily_steps, systolic, diastolic, 
        gender_male
    ] + occupation_encoded + bmi_encoded])

    # Use the model to make a prediction
    prediction = model.predict(input_data)
    
    # Convert the prediction to a readable format
    prediction_index = np.argmax(prediction, axis=1)[0]  # Get the index of the highest probability
    prediction_confidence = prediction[0][prediction_index] * 100 
    prediction_mapping = {
        0: "No Sleep Disorder",
        1: "Insomnia",
        2: "Sleep Apnea"
    }
    result = prediction_mapping.get(prediction_index, "Unknown")
    if result in ["Insomnia", "Sleep Apnea"]:
        message = gr.Markdown("# Did you know?\n ## Here are some facts related to sleep disorders:")
        image = "sleep_problems_table.png"
        source_message = (
            "Source: [AIHW - Sleep problems as a risk factor]"
            "(https://www.aihw.gov.au/reports/risk-factors/sleep-problems-as-a-risk-factor/summary)"
        )

    else:
        image = "starrysky.jpg"
        message = gr.Markdown("# Have a good night's sleep!")
        source_message = (""
        )

    confidence_message = f"**Model Confidence: {prediction_confidence:.2f}%**"

    return result, confidence_message, message, image,  source_message
    
def welcome(name):
    if not name.strip():
        return""
    return f"Nice to meet you, {name}! Let's begin."

js = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'left';
    container.style.marginBottom = '20px';

    var text = 'Welcome to the Sleep Disorder Prediction App';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.2s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 30);
            }, i * 30 );
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""
# Build the Gradio interface

with gr.Blocks(js=js) as demo:
    
    gr.Markdown("""
    This app predicts the risk of developing sleep disorders based on your responses to a series of questions.
    Please fill in the details below to get started.<br />
    <sub>*This project was built as an educational exercise during UWA's Data Analytics Bootcamp program. It was developed under a cooperative effort of Group 3
    members: Daniel Usuga, Bradley Curthoys, Lisa Shimano, and Bailey Strauch.*</sub>
    """)

    # Welcome section
    with gr.Row():
        inp = gr.Textbox(placeholder="What is your name?", show_label=False, scale=0, min_width=300)
        out = gr.Label(show_label=False, scale=1, min_width=500)
        
    with gr.Row():
        submit_btn = gr.Button("Submit", scale=0)
        submit_btn.click(fn=welcome, inputs=inp, outputs=out)
    
    with gr.Row():
        gr.Markdown("""
        <br />
        """
        )

    with gr.Row():
        gr.Markdown("## User Questionnaire")

    with gr.Row():
        gr.Markdown("""
    To make a prediction about your risk of developing a sleep disorder, please answer the questions below. All questions must be answered for the app to
    process your data correctly. You can hover over the question heading to display the categorical values associated with each question.<br />
    <br />
    ***Disclaimer:*** &nbsp;This app is intended as interactive display of a machine learning model at work ONLY. It is not to be taken as medical advice. If you think you may have
    or a be at risk of developing a sleep disorder, please consult your PCP or another licensed medical professional.
    <a href="https://www.healthdirect.gov.au/sleep-disorders" target="_blank" style="color: #2b07ed;">More information on Sleep Disorders</a>
    """)    
    
    with gr.Row():
        gender = gr.Radio(choices=["Male", "Female"], label="Biological Gender")
        age = gr.Number(label="Age", value=30)
    
    with gr.Row():

        gr.HTML("""
<style>
    .tooltip {
        position: relative;
        display: inline-block;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 465px;
        background-color: #7393B3;
        color: #fff;
        text-align: left;
        border-radius: 0px;
        padding: 5px 5px 5px 5px;
        position: absolute;
        z-index: 50;
        bottom: -250%;
        left: 100%;
        margin-left: 5px;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>

<div class="tooltip">
    <label for="sleep_duration"><b>Sleep Duration</b></label>
    <div class="tooltiptext">
        <strong>Recommended Sleep Duration (Mayo Clinic):</strong><br>
        <em>Adults:&nbsp</em> 7 or more hours per night<br>
        <em>Teens (13-18 years):&nbsp</em> 8 to 10 hours per night<br>
        <em>School-age children (6-12 years):&nbsp</em> 9 to 12 hours per night<br>
        <em>Toddlers (1-2 years):&nbsp</em> 11 to 14 hours per 24 hours (including naps)<br>
        <a href="https://www.mayoclinic.org/healthy-lifestyle/adult-health/expert-answers/how-many-hours-of-sleep-are-enough/faq-20057898" target="_blank" style="color: #add8e6;">Learn more</a>
    </div>
</div>
""")
    sleep_duration = gr.Slider(0, 12, step=0.1, label="Enter the duration of your sleep (hours)", value=7)
    
    gr.HTML("""
<style>
    .tooltip {
        position: relative;
        display: inline-block;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 465px;
        background-color: #7393B3;
        color: #fff;
        text-align: left;
        border-radius: 0px;
        padding: 5px 5px 5px 5px;
        position: absolute;
        z-index: 50;
        bottom: -250%;
        left: 100%;
        margin-left: 5px;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>

<div class="tooltip">
    <label for="quality_of_sleep"><b>Quality of Sleep<b/></label>
    <div class="tooltiptext">
        <strong>Quality of Sleep Explanation:</strong><br>
        <em>1-2:&nbsp</em> Very poor quality, frequent disturbances<br>
        <em>3-4:&nbsp</em> Poor quality, several disturbances<br>
        <em>5-6:&nbsp</em> Average quality, some disturbances<br>
        <em>7-8:&nbsp</em> Good quality, few disturbances<br>
        <em>9-10:&nbsp</em> Excellent quality, undisturbed sleep
    </div>
</div>
""")
    
    quality_of_sleep = gr.Slider(1, 10, label="Enter the quality of your sleep (1-10)", value=5)
    
    gr.HTML("""
    <style>
        .tooltip {
            position: relative;
            display: inline-block;
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            width: 465px;
            background-color: #7393B3;
            color: #fff;
            text-align: left;
            border-radius: 0px;
            padding: 5px 5px 5px 5px;
            position: absolute;
            z-index: 50;
            bottom: -250%; /* Position the tooltip above the text */
            left: 100%;
            margin-left: 5px;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>

    <div class="tooltip">
        <label for="physical_activity_level"><b>Physical Activity Level<b/></label>
        <div class="tooltiptext">
            <strong>Physical Activity Level Explanation:</strong><br>
            <em>0-20:&nbsp</em> Sedentary (little or no physical activity)<br>
            <em>21-40:&nbsp</em> Lightly active (light exercise or sports 1-3 days/week)<br>
            <em>41-60:&nbsp</em> Moderately active (moderate exercise or sports 3-5 days/week)<br>
            <em>61-80:&nbsp</em> Very active (hard exercise or sports 6-7 days a week)<br>
            <em>81-100:&nbsp</em> Super active (very hard exercise, physical job, or training twice a day)
        </div>
    </div>
    """)
    
    physical_activity_level = gr.Slider(0, 100, label="Enter your physical activity level (1-100)", value=50)

    gr.HTML("""
<style>
    .tooltip {
        position: relative;
        display: inline-block;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 465px;
        background-color: #7393B3;
        color: #fff;
        text-align: left;
        border-radius: 0px;
        padding: 5px 5px 5px 5px;
        position: absolute;
        z-index: 50;
        bottom: -250%;
        left: 100%;
        margin-left: 5px;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>

<div class="tooltip">
    <label for="stress_level"><b>Stress Level<b/></label>
    <div class="tooltiptext">
        <strong>Stress Level Explanation:</strong><br>
        <em>1-2:&nbsp</em> Very low stress, calm and relaxed<br>
        <em>3-4:&nbsp</em> Low stress, minor concerns<br>
        <em>5-6:&nbsp</em> Moderate stress, manageable but noticeable<br>
        <em>7-8:&nbsp</em> High stress, significant tension<br>
        <em>9-10:&nbsp</em> Very high stress, overwhelming and constant pressure
    </div>
</div>
""")

    stress_level = gr.Slider(1, 10, label="Enter your stress level (1-10)", value=5)
    
    with gr.Row():
        heart_rate = gr.Number(label="Heart Rate", value=70)
        daily_steps = gr.Number(label="Daily Steps", value=5000)
        systolic = gr.Number(label="Systolic Blood Pressure", value=120)
        diastolic = gr.Number(label="Diastolic Blood Pressure", value=80)
    
    with gr.Row():
        occupation = gr.Dropdown(choices=[
            "Doctor", "Engineer", "Lawyer", "Manager", "Nurse",
            "Sales Representative", "Salesperson", "Scientist", 
            "Software Engineer", "Teacher"
        ], label="Occupation")
        
        bmi_category = gr.Dropdown(choices=["Normal Weight", "Overweight", "Obese"], label="BMI Category")
    
    output = gr.Label(label="Predicted Sleep Disorder")
    confidence_output = gr.Markdown()
    message_output = gr.Markdown()
    image_output = gr.Image(show_label=False, container=False)
    source_output = gr.Markdown() 

    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=predict_sleep_disorder, 
                     inputs=[gender, age, sleep_duration, quality_of_sleep, physical_activity_level, stress_level, heart_rate, daily_steps, systolic, diastolic, occupation, bmi_category],
                     outputs=[output, confidence_output, message_output, image_output, source_output])
    
demo.launch()
