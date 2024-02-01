import simulation
import streamlit as st
import os


def main():
    """Run main function."""
    # Get yaml files
    folder_path = "./trainconfig"
    file_names = os.listdir(folder_path)
    yaml_files = [file[:-5] for file in file_names if file.endswith(".yaml")]

    # Select yaml file
    name = st.selectbox('모델 설정!!!!', yaml_files)
    
    # Select is_2d and is_3d
    is_2d = st.checkbox('2D Plot')
    is_3d = st.checkbox('3D Plot')
    
    # Simulation
    if name in yaml_files:
        try:
            sim = simulation.Simulation(name)
        except:
            st.error("해당 모델이 존재하지 않습니다.")
            return
        sim.inference()
        # Plot
        plot = simulation.Ploting(is_2d, is_3d)
        figs = plot.plot(sim)
        if is_2d:
            st.pyplot(figs[0])
        if is_3d:
            st.pyplot(figs[1])

if __name__ == '__main__':
    main()
