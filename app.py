import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

# Load merged dataset
df = pd.read_csv("fitnourish_combined_data.csv")
df.fillna("N/A", inplace=True)

# Sort dropdown list
food_names = sorted(df["Food Name"].unique().tolist())

# ------------------------
# Evaluation functions
# ------------------------

def to_float(val):
    try:
        return float(val)
    except:
        return None

def to_float(val):
    try:
        return float(val)
    except:
        return 0.0  # default for missing or N/A
def verdict(row, goal):
    cal = to_float(row["Calories"])
    prot = to_float(row["Protein (g)"])
    fat = to_float(row["Fat (g)"])
    carbs = to_float(row["Carbohydrates (g)"])

    if goal == "High‑Protein" and prot >= 15:
        return "✅ High-protein food 💪"
    if goal == "Low‑Fat" and fat <= 5:
        return "✅ Low-fat choice 🥗"
    if goal == "Bulking" and cal >= 300:
        return "✅ Great for bulking 🍚"
    if goal == "Cutting" and cal <= 150:
        return "✅ Suitable for cutting 🥦"
    return "ℹ️ General fitness food"



def macro_chart(row):
    labels = ["Calories", "Protein (g)", "Fat (g)", "Carbs (g)"]
    values = [
        to_float(row["Calories"]),
        to_float(row["Protein (g)"]),
        to_float(row["Fat (g)"]),
        to_float(row["Carbohydrates (g)"])
    ]
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=["#FFC300", "#28B463", "#FF5733", "#5DADE2"])
    ax.set_ylabel("Amount")
    ax.set_title("Macro Breakdown")
    for i, v in enumerate(values):
        ax.text(i, v + max(values)*0.02, f"{v:.1f}", ha='center')
    plt.tight_layout()
    return fig


# ------------------------
# Main function
# ------------------------

def show_nutrition(food_name, goal):
    if not food_name:
        return "❌ Please select a food item.", None

    row = df[df["Food Name"] == food_name]
    if row.empty:
        return f"❌ Food item not found: {food_name}", None

    row = row.iloc[0]
    md = f"### **{row['Food Name']}**  \n"
    md += f"*Source:* {row['Source']}  \n\n"
    md += "| Nutrient | Value |\n|---|---|\n"
    md += f"| Calories | {row['Calories']} kcal |\n"
    md += f"| Protein | {row['Protein (g)']} g |\n"
    md += f"| Fat | {row['Fat (g)']} g |\n"
    md += f"| Carbohydrates | {row['Carbohydrates (g)']} g |\n\n"
    md += verdict(row, goal)

    return md, macro_chart(row)

# ------------------------
# Gradio UI
# ------------------------

with gr.Blocks() as demo:
    gr.Markdown("## 🥗 **FitNourish** – Nutrition Info for Indian & Global Foods")
    gr.Markdown("Select a food and your fitness goal to view smart nutrition details.")

    dropdown = gr.Dropdown(choices=food_names, label="📋 Select a food item")
    goal = gr.Radio(choices=["None", "High‑Protein", "Low‑Fat", "Bulking", "Cutting"], value="None", label="🏋️ Goal Filter")

    out_md = gr.Markdown()
    out_plot = gr.Plot()

    dropdown.change(fn=show_nutrition, inputs=[dropdown, goal], outputs=[out_md, out_plot])
    goal.change(fn=show_nutrition, inputs=[dropdown, goal], outputs=[out_md, out_plot])

demo.launch()
