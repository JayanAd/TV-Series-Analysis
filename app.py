import streamlit as st
import pandas as pd
from theme_classifier import ThemeClassifier


def get_themes(theme_list_str, subtitles_path, save_path):
    st.write("Processing themes...")
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    # Remove dialogue from the theme list
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_df[theme_list]

    output_df = output_df[theme_list].sum().reset_index()
    output_df.columns = ['Theme', 'Score']

    return output_df

def main():
    st.title("Theme Classification (Zero Shot Classifiers)")

    # Theme Classification Section
    st.subheader("Classify Themes")

    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        theme_list_str = st.text_input("Enter Themes (comma-separated):")
        subtitles_path = st.text_input("Enter Subtitles or Script Path:")
        save_path = st.text_input("Enter Save Path:")
        get_themes_button = st.button("Get Themes")

    with col2:
        # Placeholder for the plot
        plot_placeholder = st.empty()
        
        if get_themes_button:
            if theme_list_str and subtitles_path and save_path:
                output_df = get_themes(theme_list_str, subtitles_path, save_path)
                plot_placeholder.write("Theme Scores")
                plot_placeholder.dataframe(output_df)
                plot_placeholder.bar_chart(output_df.set_index('Theme'))
            else:
                st.warning("Please fill in all the fields to get themes.")

    

if __name__ == '__main__':
    main()
