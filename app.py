import altair as alt
import pandas as pd
import streamlit as st

st.title("Palmer's Penguins")
st.markdown("Use this Streamlit app to make your own scatterplot about penguins!")

penguins_df = pd.read_csv('penguins.csv')

features = penguins_df.select_dtypes(include=["number"]).columns.tolist()
features = [col for col in features if col not in ["year","rowid"]]

selected_x_var = st.selectbox(
    "What do you want the x variable to be?",
    features,
)
selected_y_var = st.selectbox(
    "What about the y?",
    features,
)

# penguin_file = st.file_uploader("Select Your Local Penguins CSV")
# if penguin_file is not None:
#    penguins_df = pd.read_csv(penguin_file)
# else:
#    st.stop()

alt_chart = (
    alt.Chart(penguins_df, title="Scatterplot of Palmer's Penguins")
    .mark_circle()
    .encode(
        x=alt.X(selected_x_var, scale=alt.Scale(zero=False)),
        y=alt.Y(selected_y_var, scale=alt.Scale(zero=False)),
        color="species",
    )
    .interactive()
)
st.altair_chart(alt_chart, use_container_width=True)