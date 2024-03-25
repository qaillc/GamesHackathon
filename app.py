import streamlit as st
import pandas as pd
import plotly.express as px
import time
import ast  # To safely evaluate string literals as Python expressions

st.set_page_config(layout="wide")
st.title("Games - Gemini Ultra Simulator")


positions_text = """Agents: Clara (-3,3), Eddie (3,3), Sofia (-3,-3), Alex (3,-3)"""



# Load the positions data from the specified path
positions_df = pd.read_csv('./data/positions.csv')

# Correctly use the 'positions' column name with lowercase 'p' for the ast.literal_eval conversion
positions_df['positions'] = positions_df['positions'].apply(ast.literal_eval)


# Initialize or get the current animation state (paused or playing)
if 'paused' not in st.session_state:
    st.session_state['paused'] = False

# Create two columns in the Streamlit app
left_column, right_column = st.columns(2)



# Define the text you want to display in the text box
course_goal = """
I am developing a course focused on conducting effective meetings. To achieve this, I require a team of specialists, each assigned roles that are instrumental in the course development process, such as author, editor, critic, and so forth. I need detailed profiles for these team members, including their names, assigned tasks, goals, and backstories.
"""
course_agents = """
1. Agent Name: Clara "The Conductor" Williams
Role: Lead Author
Tasks:
- Develop core course outline
- Create engaging lesson plans & activities
- Research and integrate best practices
- Write clear and concise scripts
Goals:
- Make meetings a source of productivity, not dread
- Transform meeting culture in workplaces
Backstory: Ex-management consultant frustrated with wasted hours in unproductive meetings. Passionate about efficiency and turning meetings into problem-solving powerhouses.

2. Agent Name: Eddie "Eagle Eye" Thompson
Role: Editor & Quality Control
Tasks:
- Review content for clarity and flow
- Ensure examples are relevant and impactful
- Fact-check all information
- Maintain consistent course voice/tone
Goals:
- Deliver a polished and credible course
- Catch any errors or inconsistencies
Backstory: Former journalist with a keen eye for detail and accuracy. Believes that well-crafted content is essential for effective learning.

3. Agent Name: Sofia "The Skeptic" Ramirez
Role: Critic and User Advocate
Tasks:
- Ask tough questions about content and approach
- Challenge assumptions about learner needs
- Test activities, visuals, and examples for usability
- Provide feedback from a realistic learner's perspective
Goals:
- Bulletproof the course against common pitfalls
- Ensure it resonates with diverse audiences
Backstory: Seasoned HR professional who's seen the good, the bad, and the ugly of workplace meetings. Wants courses to be truly transformative, not just theoretical.

4. Agent Name: Alex "The Innovator" Kim
Role: Multimedia Specialist
Tasks:
- Design engaging visuals (infographics, illustrations)
- Source or create short video clips
- Develop interactive elements
- Ensure seamless integration of multimedia into the course
Goals:
- Break down complex concepts visually
- Make the course dynamic and memorable
Backstory: Graphic designer turned instructional design enthusiast. Believes learning should be as visually appealing as it is informative.
"""

course_outline = """
Module 1: The Meeting Mindset

Step 1: Why Meetings (Sometimes) Get a Bad Rap
Common meeting complaints and frustrations
The true costs of unproductive meetings
The potential benefits of well-run meetings
Step 2: Before You Hit "Schedule": Meeting or Memo?
Decision tree: Does this topic truly need a meeting?
When asynchronous communication is better
Alternatives to traditional meetings (standups, quick huddles, etc.)
Step 3: The Power of Purpose
Defining clear meeting goals (decision-making, information sharing, brainstorming, etc.)
SMART objectives for meetings

Module 2: Preparation is Everything

Step 1: The Anatomy of an Effective Agenda
Template and samples of great agendas
Time allocation and prioritization
Building in time for discussion, not just report-outs
Step 2: Right People, Right Roles
Avoiding the "invite everyone" trap
Identifying essential attendees vs. optional
Assigning pre-meeting prep (if needed)
Step 3: Setting the Stage
Tech checks for smoother virtual meetings
Room setup considerations (in-person)

Module 3: Masterful Meeting Facilitation

Step 1: Strong Starts and Focused Guidance
Opening the meeting with purpose
Ground rules and participation norms
Techniques to keep things on track
Step 2: Inclusive Participation
Encouraging contributions from all attendees
Dealing with dominant personalities tactfully
Handling tangents and side conversations
Step 3: Decision-Making and Action Items
Reaching consensus vs. voting
Clear ownership of action items
Summarizing key takeaways

Module 4: Dealing with Disruptions

Step 1: Common Meeting Derailers
The rambler, the tech difficulties, the unprepared, etc.
Strategies for addressing each with respect
Step 2: Conflict and Difficult Dynamics
Diffusing tension
When to table topics for later
Step 3: Debrief and Improvement
Quick post-meeting evaluation
Implementing feedback for future meetings

"""



# Use the text_area widget to display the information in a non-editable, scrollable text box

common_goal = left_column.text_area("Goal", value=course_goal, height=100)

common_agents = left_column.text_area("Agents", value=course_agents, height=400)

common_outline= left_column.text_area("Chain of Thought Outline", value=course_outline, height=400)


# Move the pause/play button under the common goal on the right side
#if left_column.button('Pause' if not st.session_state['paused'] else 'Play'):
#    st.session_state['paused'] = not st.session_state['paused']

# Placeholder for the Plotly chart in the right column


    
chart_placeholder = right_column.empty()

markdonw_position = right_column.markdown(f"```\n{positions_text}\n```")

animation_speed = right_column.slider("Animation Speed (Seconds per Frame)", 1, 10, 2, key='animation_speed')


# Placeholder for displaying additional data below the chart.
data_placeholder = right_column.empty()


# Placeholder for displaying the data below the animation
data_placeholder = right_column.empty()

# Initialize an index to keep track of the current frame (row) to display
current_frame = 0

while True:
    if not st.session_state['paused']:
        # Fetch the current row based on the frame index
        row = positions_df.iloc[current_frame % len(positions_df)]
        positions = row['positions']  # Access the 'positions' column with lowercase 'p'

        # Prepare data for plotting
        new_data_points = [{'Agent': agent, 'x': position[0], 'y': position[1]} for agent, position in positions.items()]
        new_data = pd.DataFrame(new_data_points)

        # Create a new Plotly figure for the scatter plot, using Agent names for color distinction
        fig = px.scatter(new_data, x='x', y='y', color='Agent', title="Agent Positions")

        # Update figure layout
        fig.update_layout(xaxis_title='X Axis', yaxis_title='Y Axis', autosize=True, xaxis=dict(range=[-5, 5]), yaxis=dict(range=[-5, 5]))

        # Update traces to adjust the appearance of the dots, setting radius to 10 (size 20 for visual effect)
        fig.update_traces(marker=dict(size=20))

        # Display the figure in the right column
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        # Clear previous data display and show new data for the current frame
        data_display = ""
        for column_name, value in row.drop('positions').items():
            data_display += f"**{column_name}:** {value}\n\n"
        data_placeholder.markdown(data_display)

        # Increment the frame index to display the next set of positions
        current_frame += 1

    # Use the slider value for the sleep duration
    time.sleep(st.session_state['animation_speed'])