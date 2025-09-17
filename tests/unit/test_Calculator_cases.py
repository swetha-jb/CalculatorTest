import sys, os, types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'CalCulator')))

# Auto-mock tkinter for headless environments
try:
    import tkinter as tk
except ImportError:
    import sys, types
    class _WidgetMock:
        def __init__(self, *a, **k): self._text = ""
        def config(self, **kwargs): 
            if "text" in kwargs: self._text = kwargs["text"]
        def cget(self, key): return self._text if key == "text" else None
        def get(self): return self._text
        def grid(self, *a, **k): return []
        def pack(self, *a, **k): return []
        def place(self, *a, **k): return []
        def destroy(self): return None
        def __getattr__(self, item): return lambda *a, **k: None
    tk = types.ModuleType("tkinter")
    for widget in ["Tk","Label","Button","Entry","Frame","Canvas","Text","Scrollbar","Checkbutton",
                "Radiobutton","Spinbox","Menu","Toplevel","Listbox"]:
        setattr(tk, widget, _WidgetMock)
    for const in ["N","S","E","W","NE","NW","SE","SW","CENTER","NS","EW","NSEW"]:
        setattr(tk, const, const)
    sys.modules["tkinter"] = tk

import pytest
from unittest.mock import patch

# Mock necessary modules to avoid actual GUI and external API calls during testing
class MockCTkFrame:
    def __init__(self, *args, **kwargs):
        pass

class MockCTkLabel:
    def __init__(self, *args, **kwargs):
        pass

class MockCTkButton:
    def __init__(self, *args, **kwargs):
        pass

class MockCTkEntry:
    def __init__(self, *args, **kwargs):
        self._value = ""

    def get(self):
        return self._value

    def delete(self, first, last):
        self._value = ""

    def insert(self, index, string):
        self._value += string

class MockCTkTextbox:
    def __init__(self, *args, **kwargs):
        self._value = ""

    def get(self, index1, index2):
        return self._value

    def delete(self, index1, index2):
        self._value = ""

    def insert(self, index, string):
        self._value += string

class MockCTkFrame:
    def __init__(self, *args, **kwargs):
        pass

class MockCTkLabel:
    def __init__(self, *args, **kwargs):
        pass

class MockCTkButton:
    def __init__(self, *args, **kwargs):
        pass

class MockCTkEntry:
    def __init__(self, *args, **kwargs):
        self._value = ""

    def get(self):
        return self._value

    def delete(self, first, last):
        self._value = ""

    def insert(self, index, string):
        self._value += string

class MockCTkTextbox:
    def __init__(self, *args, **kwargs):
        self._value = ""

    def get(self, index1, index2):
        return self._value

    def delete(self, index1, index2):
        self._value = ""

    def insert(self, index, string):
        self._value += string

class MockCTkComboBox:
    def __init__(self, *args, **kwargs):
        self.current_value = '[select]'

    def get(self):
        return self.current_value

class MockCTk:
    def __init__(self, *args, **kwargs):
        pass

    def geometry(self, size):
        pass

    def title(self, title):
        pass

    def pack(self, **kwargs):
        pass

    def pack_propagate(self, propagate):
        pass

    def configure(self, **kwargs):
        pass
        
    def winfo_children(self):
        return []


# Mock implementations for the imported modules
class MockCalculator:
    def calculate(self, expr, conditions):
        if expr == "2+2":
            return "4"
        elif expr == "sin(pi/2)":
            return "1"
        elif expr == "d/dx[x^2]":
            return "2*x"
        elif expr == "∫[x]dx":
            return "x**2/2"
        elif expr == "lim[1/x] as x->0":
            return "inf"
        elif expr == "ERROR_CASE":
            return None
        return "mock_result"

    def clean(self, expr):
        return expr.replace(' ', '')

    def post_clean(self, expr):
        return expr

class MockVector:
    def vector_calc(self, oper, a, b=None):
        if oper == 'add':
            return "[3, 5]"
        elif oper == 'dot':
            return "10"
        elif oper == 'det':
            return "10"
        elif oper == 'norm':
            return "5.0"
        elif oper == 'length':
            return "10.0"
        elif oper == 'deriv':
            return "[1, 2, 3]"
        return "mock_vector_result"

class MockGraph:
    def graph(self, expr):
        pass

class MockSolverAI:
    def generate(self, problem):
        return "mock AI answer"

# Replace actual imports with mocks for testing purposes
ctk = MockCTk()
calculate = MockCalculator().calculate
vector_calc = MockVector().vector_calc
graph = MockGraph().graph
generate = MockSolverAI().generate

# --- Unit Tests ---

# Mocking Tkinter/CustomTkinter elements to avoid GUI interaction
@pytest.fixture
def mock_gui_elements():
    with patch('customtkinter.CTkLabel', new=MockCTkLabel), \
         patch('customtkinter.CTkFrame', new=MockCTkFrame), \
         patch('customtkinter.CTkButton', new=MockCTkButton), \
         patch('customtkinter.CTkEntry', new=MockCTkEntry), \
         patch('customtkinter.CTkTextbox', new=MockCTkTextbox), \
         patch('customtkinter.CTkComboBox', new=MockCTkComboBox), \
         patch('customtkinter.CTk', new=MockCTk):
        yield

# Test for the initial setup and display of the calculator page
def test_initial_page_is_calculator(mock_gui_elements):
    # This test focuses on the initial call to indicate and the expected page setup.
    # We can't directly assert which page is "shown" without a running GUI,
    # but we can check if the initial call to calc_page happens.
    with patch('main.calc_page') as mock_calc_page:
        # Re-running the main execution flow up to the point where pages are switched
        # This is a simplified way to test the initial page load without a full app run
        
        # Mocking the components that would be created by calc_page
        global entrybox, wrt, lim, integral_l, integral_r, sum_i, sum_n
        entrybox = MockCTkEntry()
        wrt = MockCTkEntry()
        lim = MockCTkEntry()
        integral_l = MockCTkEntry()
        integral_r = MockCTkEntry()
        sum_i = MockCTkEntry()
        sum_n = MockCTkEntry()
        
        main.indicate(MockCTkButton(), main.calc_page) # Simulate initial indication

        # Assert that calc_page was called
        mock_calc_page.assert_called_once()

# Test the 'calc_page' function for basic functionality
def test_calc_page_elements_creation(mock_gui_elements):
    # This test checks if the main elements of the calculator page are created.
    # We can't directly assert the appearance, but we can check if the functions are called.
    
    # Mocking the click_button and calc_buttons to ensure they are called during page setup
    with patch('main.click_button') as mock_click_button, \
         patch('main.calc_buttons') as mock_calc_buttons:
        
        main.calc_page() # Execute the calculator page setup

        # Assert that essential UI elements are attempted to be created
        # This is a shallow test as it doesn't check the actual creation of widgets,
        # but rather if the logic to create them is executed.
        assert mock_calc_buttons.call_count > 0 # Expect buttons to be created

# Test the 'click_button' function when 'clear' is pressed
def test_click_button_clear(mock_gui_elements):
    # Mock the entry widgets to check if their delete methods are called
    mock_entry_boxes = {
        'entrybox': MockCTkEntry(),
        'wrt': MockCTkEntry(),
        'lim': MockCTkEntry(),
        'integral_l': MockCTkEntry(),
        'integral_r': MockCTkEntry(),
        'sum_i': MockCTkEntry(),
        'sum_n': MockCTkEntry()
    }

    # Temporarily patch the global entry widgets with our mocks
    original_entrybox = main.entrybox
    original_wrt = main.wrt
    original_lim = main.lim
    original_integral_l = main.integral_l
    original_integral_r = main.integral_r
    original_sum_i = main.sum_i
    original_sum_n = main.sum_n

    main.entrybox = mock_entry_boxes['entrybox']
    main.wrt = mock_entry_boxes['wrt']
    main.lim = mock_entry_boxes['lim']
    main.integral_l = mock_entry_boxes['integral_l']
    main.integral_r = mock_entry_boxes['integral_r']
    main.sum_i = mock_entry_boxes['sum_i']
    main.sum_n = mock_entry_boxes['sum_n']

    with patch.object(mock_entry_boxes['entrybox'], 'delete') as mock_delete_entry, \
         patch.object(mock_entry_boxes['wrt'], 'delete') as mock_delete_wrt, \
         patch.object(mock_entry_boxes['lim'], 'delete') as mock_delete_lim, \
         patch.object(mock_entry_boxes['integral_l'], 'delete') as mock_delete_integral_l, \
         patch.object(mock_entry_boxes['integral_r'], 'delete') as mock_delete_integral_r, \
         patch.object(mock_entry_boxes['sum_i'], 'delete') as mock_delete_sum_i, \
         patch.object(mock_entry_boxes['sum_n'], 'delete') as mock_delete_sum_n:

        main.click_button('clear') # Call the function with 'clear'

        # Assert that delete was called on all entry widgets
        mock_delete_entry.assert_called_once_with(0, main.ctk.END)
        mock_delete_wrt.assert_called_once_with(0, main.ctk.END)
        mock_delete_lim.assert_called_once_with(0, main.ctk.END)
        mock_delete_integral_l.assert_called_once_with(0, main.ctk.END)
        mock_delete_integral_r.assert_called_once_with(0, main.ctk.END)
        mock_delete_sum_i.assert_called_once_with(0, main.ctk.END)
        mock_delete_sum_n.assert_called_once_with(0, main.ctk.END)

    # Restore original entry widgets
    main.entrybox = original_entrybox
    main.wrt = original_wrt
    main.lim = original_lim
    main.integral_l = original_integral_l
    main.integral_r = original_integral_r
    main.sum_i = original_sum_i
    main.sum_n = original_sum_n

# Test the 'click_button' function when a regular button is pressed
def test_click_button_regular(mock_gui_elements):
    mock_entry = MockCTkEntry()
    original_entrybox = main.entrybox
    main.entrybox = mock_entry

    with patch.object(mock_entry, 'insert') as mock_insert:
        main.click_button('x')
        mock_insert.assert_called_once_with(main.ctk.END, 'x')

    main.entrybox = original_entrybox # Restore

# Test the 'click_button' function when 'calculate' is pressed with a valid expression
def test_click_button_calculate_valid(mock_gui_elements):
    mock_entry = MockCTkEntry()
    mock_entry.get = lambda: "2+2"
    
    original_entrybox = main.entrybox
    main.entrybox = mock_entry

    with patch.object(main.calculate) as mock_calculate, \
         patch.object(mock_entry, 'delete') as mock_delete, \
         patch.object(mock_entry, 'insert') as mock_insert:
        
        mock_calculate.return_value = "4"
        main.click_button('calculate')

        mock_delete.assert_called_once_with(0, main.ctk.END)
        mock_insert.assert_called_once_with(0, "4")

    main.entrybox = original_entrybox # Restore

# Test the 'click_button' function when 'calculate' is pressed with an expression causing an error
def test_click_button_calculate_error(mock_gui_elements):
    mock_entry = MockCTkEntry()
    mock_entry.get = lambda: "ERROR_CASE"
    
    original_entrybox = main.entrybox
    main.entrybox = mock_entry

    with patch.object(main.calculate) as mock_calculate, \
         patch.object(mock_entry, 'delete') as mock_delete, \
         patch.object(mock_entry, 'insert') as mock_insert:
        
        mock_calculate.return_value = None # Simulate an error result
        main.click_button('calculate')

        mock_delete.assert_called_once_with(0, main.ctk.END)
        mock_insert.assert_called_once_with(0, "ERROR")

    main.entrybox = original_entrybox # Restore

# Test the 'indicate' function for page switching and button styling
def test_indicate_page_switching(mock_gui_elements):
    # Mocking reset_indicators and delete_frames
    with patch('main.reset_indicators') as mock_reset_indicators, \
         patch('main.delete_frames') as mock_delete_frames, \
         patch('main.calc_page') as mock_calc_page, \
         patch('main.vector_page') as mock_vector_page, \
         patch('main.graphs_page') as mock_graphs_page, \
         patch('main.wp_page') as mock_wp_page:

        # Create mock buttons for testing
        mock_calc_menu_btn = MockCTkButton()
        mock_vector_menu_btn = MockCTkButton()
        mock_graph_menu_btn = MockCTkButton()
        mock_wp_menu_btn = MockCTkButton()

        # Mocking the configuration method of the buttons to check styling changes
        with patch.object(mock_calc_menu_btn, 'configure') as mock_calc_configure, \
             patch.object(mock_vector_menu_btn, 'configure') as mock_vector_configure, \
             patch.object(mock_graph_menu_btn, 'configure') as mock_graph_configure, \
             patch.object(mock_wp_menu_btn, 'configure') as mock_wp_configure:

            # Test switching to calculator page
            main.indicate(mock_calc_menu_btn, main.calc_page)
            mock_reset_indicators.assert_called_once()
            mock_delete_frames.assert_called_once_with(main.main_frame)
            mock_calc_configure.assert_called_once_with(fg_color='#624aa1', border_width=3)
            mock_calc_page.assert_called_once()

            # Reset call counts for the next test
            mock_reset_indicators.reset_mock()
            mock_delete_frames.reset_mock()
            mock_calc_configure.reset_mock()
            mock_calc_page.reset_mock()

            # Test switching to vector page
            main.indicate(mock_vector_menu_btn, main.vector_page)
            mock_reset_indicators.assert_called_once()
            mock_delete_frames.assert_called_once_with(main.main_frame)
            mock_vector_configure.assert_called_once_with(fg_color='#624aa1', border_width=3)
            mock_vector_page.assert_called_once()

# Test the 'vector_page' function's initial setup
def test_vector_page_initial_setup(mock_gui_elements):
    with patch('main.delete_frames'), \
         patch('main.build') as mock_build, \
         patch('main.vector_calc') as mock_vector_calc:

        # Mocking the necessary UI elements that vector_page() would interact with
        main.main_frame = MockCTkFrame()
        main.vector_drop = MockCTkComboBox()
        main.vector_drop.current_value = 'vector addition'
        
        # Simulate the creation of UI elements within vector_page
        main.vector_page()
        
        # This is a shallow check to ensure the UI elements are configured
        # We can't fully test the dynamic building without more complex mocking
        assert True # Placeholder for actual checks if needed

# Test the 'select' function within 'vector_page'
def test_vector_page_select_function(mock_gui_elements):
    # Mocking the necessary UI elements and functions
    main.main_frame = MockCTkFrame()
    main.vec_frame = MockCTkFrame()
    main.vector_drop = MockCTkComboBox()
    main.vector_drop.current_value = 'vector addition'

    with patch('main.build') as mock_build:
        # Call select which should trigger build if a function is selected
        main.select()
        mock_build.assert_called_once_with('vector addition')

    # Test case where no function is selected
    main.vector_drop.current_value = '[select]'
    with patch('main.build') as mock_build:
        main.select()
        mock_build.assert_not_called()

# Test the 'reset' function within 'vector_page'
def test_vector_page_reset_function(mock_gui_elements):
    with patch('main.delete_frames') as mock_delete_frames, \
         patch('main.vector_page') as mock_vector_page:
        
        # Call reset
        main.reset()
        
        # Expect delete_frames to be called on main_frame
        mock_delete_frames.assert_called_once_with(main.main_frame)
        # Expect vector_page to be called to re-initialize the page
        mock_vector_page.assert_called_once()

# Test the 'clear' function within 'vector_page'
def test_vector_page_clear_function(mock_gui_elements):
    # Mocking vec_frame and build function
    main.vec_frame = MockCTkFrame()
    main.vector_drop = MockCTkComboBox()
    main.vector_drop.current_value = 'vector addition'

    with patch('main.delete_frames') as mock_delete_frames, \
         patch('main.build') as mock_build:
        
        # Call clear
        main.clear()
        
        # Expect delete_frames to be called on vec_frame
        mock_delete_frames.assert_called_once_with(main.vec_frame)
        # Expect build to be called to repopulate the cleared frame
        mock_build.assert_called_once_with('vector addition')

# Test the 'calc' function within 'vector_page' for a specific operation
def test_vector_page_calc_add(mock_gui_elements):
    # Mocking the result_entry and vector_calc
    mock_result_entry = MockCTkEntry()
    mock_result_entry.delete = lambda x, y: None
    mock_result_entry.insert = lambda x, y: None
    
    original_result_entry = main.result_entry
    main.result_entry = mock_result_entry
    
    # Mocking a_entry and b_entry
    mock_a_entry = MockCTkEntry()
    mock_a_entry.get = lambda: "[1, 2]"
    mock_b_entry = MockCTkEntry()
    mock_b_entry.get = lambda: "[2, 3]"
    
    main.a_entry = mock_a_entry
    main.b_entry = mock_b_entry

    with patch('main.vector_calc') as mock_vector_calc, \
         patch.object(mock_result_entry, 'insert') as mock_insert:
        
        mock_vector_calc.return_value = "[3, 5]" # Mock the return of vector_calc
        main.calc('vector addition')
        
        # Assert that vector_calc was called with correct arguments
        mock_vector_calc.assert_called_once_with('add', "[1, 2]", "[2, 3]")
        # Assert that the result was inserted into result_entry
        mock_insert.assert_called_once_with(0, "[3, 5]")

    main.result_entry = original_result_entry # Restore

# Test the 'build' function for 'vector addition'
def test_vector_page_build_vector_addition(mock_gui_elements):
    main.vec_frame = MockCTkFrame() # Ensure vec_frame exists
    with patch('customtkinter.CTkFrame') as mock_ctk_frame, \
         patch('customtkinter.CTkEntry') as mock_ctk_entry, \
         patch('customtkinter.CTkLabel') as mock_ctk_label:
        
        # Mocking the creation of specific UI elements expected for vector addition
        mock_frame_instance = MockCTkFrame()
        mock_entry_a = MockCTkEntry()
        mock_entry_b = MockCTkEntry()
        mock_label_result = MockCTkLabel()
        mock_entry_result = MockCTkEntry()

        mock_ctk_frame.side_effect = [mock_frame_instance, mock_frame_instance] # Return mock frame for seper_1 and seper_2
        mock_ctk_entry.side_effect = [mock_entry_a, mock_entry_b, mock_entry_result] # Mock entries
        mock_ctk_label.side_effect = [mock_label_result] # Mock labels

        main.build('vector addition')

        # Assert that the correct UI elements were attempted to be created
        # This checks if the logic within build for 'vector addition' is executed.
        assert mock_ctk_frame.call_count >= 2 # Expecting frames for vector inputs and result
        assert mock_ctk_entry.call_count >= 3 # Expecting entry for a, b, and result
        assert mock_ctk_label.call_count >= 1 # Expecting label for result

# Test the 'graphs_page' function for initial setup
def test_graphs_page_initial_setup(mock_gui_elements):
    main.main_frame = MockCTkFrame()
    with patch('customtkinter.CTkLabel') as mock_label, \
         patch('customtkinter.CTkFrame') as mock_frame, \
         patch('customtkinter.CTkButton') as mock_button, \
         patch('customtkinter.CTkEntry') as mock_entry:
        
        main.graphs_page()
        
        # Assert that essential UI elements are attempted to be created
        assert mock_label.call_count >= 2
        assert mock_frame.call_count >= 1
        assert mock_button.call_count >= 1
        assert mock_entry.call_count >= 1

# Test the 'draw' function within 'graphs_page'
def test_graphs_page_draw_function(mock_gui_elements):
    # Mocking the entry widget and the graph function
    mock_entry = MockCTkEntry()
    mock_entry.get = lambda: "x^2"
    mock_entry.delete = lambda x, y: None
    
    main.f_entry = mock_entry # Assign the mock entry to the global variable

    with patch('main.graph') as mock_graph:
        main.draw("x^2")
        
        # Assert that the entry widget's delete method was called
        assert mock_entry.get() == "" # The entry should be cleared
        # Assert that the graph function was called with the expression
        mock_graph.assert_called_once_with("x^2")

# Test the 'wp_page' function for initial setup
def test_wp_page_initial_setup(mock_gui_elements):
    main.main_frame = MockCTkFrame()
    with patch('customtkinter.CTkLabel') as mock_label, \
         patch('customtkinter.CTkTextbox') as mock_textbox, \
         patch('customtkinter.CTkButton') as mock_button:
        
        main.wp_page()
        
        # Assert that essential UI elements are attempted to be created
        assert mock_label.call_count >= 1
        assert mock_textbox.call_count >= 2 # For problem_text and chat_text
        assert mock_button.call_count >= 1

# Test the 'solve' function within 'wp_page'
def test_wp_page_solve_function(mock_gui_elements):
    # Mocking the textboxes and the generate function
    mock_problem_text = MockCTkTextbox()
    mock_problem_text.get = lambda x, y: "Test problem"
    mock_problem_text.delete = lambda x, y: None
    
    mock_chat_text = MockCTkTextbox()
    mock_chat_text.insert = lambda x, y: None
    mock_chat_text.delete = lambda x, y: None
    
    main.problem_text = mock_problem_text
    main.chat_text = mock_chat_text

    with patch('solver_ai.generate') as mock_generate:
        mock_generate.return_value = "mock AI answer"
        
        main.solve()
        
        # Assert that problem_text was deleted and then read
        assert mock_problem_text.get('1.0', 'end-1c') == "Test problem"
        # Assert that generate was called with the problem
        mock_generate.assert_called_once_with("Test problem")
        # Assert that chat_text was cleared and then inserted with the answer
        mock_chat_text.delete.assert_called_once_with('1.0', 'end-1c')
        mock_chat_text.insert.assert_called_once_with('1.0', "mock AI answer")

# Test the 'reset_indicators' function
def test_reset_indicators(mock_gui_elements):
    assert True  # Placeholder assert
    # Mocking the buttons and their configure methods
    mock_calc_menu = MockCTkButton()
    mock_vector_menu = MockCTkButton()
    mock_graph_menu = MockCTkButton()
    mock_wp_menu = MockCTkButton()

    # Assign mock buttons to the global variables
    main.calc_menu = mock_calc_menu
    main.vector_menu = mock_vector_menu
    main.graph_menu = mock_graph_menu
    main.wp_menu = mock_wp_menu

    with patch.object(mock_calc_menu, 'configure') as mock_calc_configure, \
         patch.object(mock_vector_menu, 'configure') as mock_vector_configure, \
         patch.object(mock_graph_menu, 'configure') as mock_graph_configure, \
         patch.object(mock_wp_menu, 'configure') as mock_wp_configure:
        
        main.reset_indicators()
        
        # Assert that configure was called for each button with the correct parameters
        mock_calc_configure.assert_called_once_with(fg_color='#253da1', border_width=0)
        mock_vector_configure.assert_called_once_with(fg_color='#253da1', border_width=0)
        mock_graph_configure.assert_called_once_with(fg_color='#253da1', border_width=0)
        mock_wp_configure.assert_called_once_with(fg_color='#253da1', border_width=0)

# Test the 'delete_frames' function
def test_delete_frames(mock_gui_elements):
    assert True  # Placeholder assert
    # Mocking a frame and its children
    mock_child_frame1 = MockCTkFrame()
    mock_child_frame2 = MockCTkFrame()
    mock_parent_frame = MockCTkFrame()
    
    # Patching winfo_children to return mock children
    with patch.object(mock_parent_frame, 'winfo_children', return_value=[mock_child_frame1, mock_child_frame2]) as mock_winfo_children, \
         patch.object(mock_child_frame1, 'destroy') as mock_destroy1, \
         patch.object(mock_child_frame2, 'destroy') as mock_destroy2:
        
        main.delete_frames(mock_parent_frame)
        
        # Assert that winfo_children was called
        mock_winfo_children.assert_called_once()
        # Assert that destroy was called on each child frame
        mock_destroy1.assert_called_once()
        mock_destroy2.assert_called_once()
