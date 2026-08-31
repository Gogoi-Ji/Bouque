import streamlit as st
from manim import *
import numpy as np

st.title("Munim's Mathematical Flower Bouquet")
st.write("Click the button below to generate the live Manim animation.")

# Wrap your animation inside a button trigger
if st.button("Render Bouquet Animation"):
    with st.spinner("Generating beautiful shapes... Please wait..."):
        
        # This is your exact code structure inside a custom config context
        with tempconfig({"quality": "low_quality", "preview": False}):
            class Bouquet(Scene):
                def construct(self):
                    TIE_POINT = np.array([0, -4.5, 0])

                    def create_flower(numerator, denominator, colors, center, scale=1.5, leaf_dir=RIGHT):
                        def rose_equation(t):
                            r = scale * np.cos((numerator / denominator) * t)
                            x = r * np.cos(t)
                            y = r * np.sin(t)
                            return np.array([x, y, 0])
                        
                        max_t = denominator * 2 * PI
                        rose = ParametricFunction(rose_equation, t_range=[0, max_t], stroke_width=3).set_color_by_gradient(*colors).shift(center)
                        
                        p1, p4 = center, TIE_POINT
                        p2 = p1 + DOWN * 1.5
                        p3 = p4 + UP * 2.0 + (p1 - p4) * 0.1
                        stem = CubicBezier(p1, p2, p3, p4, color=GREEN, stroke_width=4)
                        
                        leaf_start = stem.point_from_proportion(0.45)
                        leaf_end = leaf_start + leaf_dir * 1.2 + UP * 0.8
                        leaf_edge1 = ArcBetweenPoints(leaf_start, leaf_end, angle=PI/3)
                        leaf_edge2 = ArcBetweenPoints(leaf_start, leaf_end, angle=-PI/3)
                        leaf = VGroup(leaf_edge1, leaf_edge2).set_color(GREEN).set_fill(GREEN_E, opacity=0.8)
                        
                        return VGroup(stem, leaf, rose)

                    back_left = create_flower(7, 4, [PINK, MAROON], np.array([-2.2, 1.5, 0]), scale=1.3, leaf_dir=LEFT)
                    back_right = create_flower(5, 2, [YELLOW, ORANGE], np.array([2.2, 1.5, 0]), scale=1.3, leaf_dir=RIGHT)
                    top_center = create_flower(8, 3, [RED, ORANGE], np.array([0, 2.8, 0]), scale=1.5, leaf_dir=RIGHT)
                    mid_left = create_flower(6, 1, [BLUE, TEAL], np.array([-1.5, -0.2, 0]), scale=1.1, leaf_dir=LEFT)
                    mid_right = create_flower(4, 1, [PURPLE, PINK], np.array([1.5, -0.2, 0]), scale=1.1, leaf_dir=RIGHT)
                    front_center = create_flower(5, 3, [WHITE, YELLOW], np.array([0, -1.2, 0]), scale=1.4, leaf_dir=LEFT)

                    bouquet = VGroup(back_left, back_right, top_center, mid_left, mid_right, front_center)

                    self.play(AnimationGroup(*[Create(flower) for flower in bouquet], lag_ratio=0.15), run_time=7, rate_func=linear)
                    
                    fills = [
                        back_left[2].animate.set_fill(PINK, opacity=0.9),
                        back_right[2].animate.set_fill(YELLOW, opacity=0.9),
                        top_center[2].animate.set_fill(RED, opacity=0.9),
                        mid_left[2].animate.set_fill(BLUE, opacity=0.9),
                        mid_right[2].animate.set_fill(PURPLE, opacity=0.9),
                        front_center[2].animate.set_fill(WHITE, opacity=0.9),
                    ]
                    self.play(*fills, run_time=2.5)
                    self.play(bouquet.animate.scale(1.05), rate_func=there_and_back, run_time=1.5)
                    self.wait(2)

            # Render the scene programmatically
            scene = Bouquet()
            scene.render()
            
            # Display the video output on the web app page
            st.video(scene.renderer.file_writer.movie_file_path)
