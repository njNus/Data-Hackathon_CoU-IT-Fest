import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import uuid

# Set up the background and font colors
# Dark Mode Toggle
# Dark mode toggle in the sidebar
# Dark mode toggle
dark_mode = st.sidebar.checkbox("Enable Dark Mode")

# Define CSS styles for dark and light modes with a colored sidebar background
dark_css = """
<style>
    .main {background-color: #1a1a1a;} /* Dark background */
    .sidebar .sidebar-content {background-color: #2b2b73;} /* Custom dark sidebar color */
    .reportview-container .markdown-text-container, .stText, .stTitle, .stButton>button {color: #ffffff;} /* White text for main content and buttons */
    h1, h2, h3 {color: #ffffff !important;} /* White text for headers */
    .stButton>button {background-color: #ff6f61; color: white;} /* Button styling */
</style>
"""

light_css = """
<style>
    .main {background-color: #ffffff;} /* Light background */
    .sidebar .sidebar-content {background-color: #cfe2f3;} /* Custom light sidebar color */
    .reportview-container .markdown-text-container, .stText, .stTitle, .stButton>button {color: #000000;} /* Black text for main content and buttons */
    h1, h2, h3 {color: #000000 !important;} /* Black text for headers */
    .stButton>button {background-color: #ff6f61; color: white;} /* Button styling */
</style>
"""

# Apply the CSS based on dark mode selection
if dark_mode:
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    st.markdown(light_css, unsafe_allow_html=True)

# Title with team name
st.markdown("<h1 style='text-align: center;'>☕ Team: 3amigos ☕</h1>", unsafe_allow_html=True)

# Sidebar navigation with icons
# Sidebar navigation with icons as buttons
st.sidebar.title("Navigation")

# Dictionary mapping page names to display labels with icons
pages = {
    "Home": "🏠 Home",
    "Level 1": "📈 Level 1",
    "Level 2": "📊 Level 2",
    "Level 3": "💡 Level 3"
}

# Initialize a session state variable to store the current page if it doesn't already exist
if "page_selection" not in st.session_state:
    st.session_state.page_selection = "Home"  # Default page

# Render each page as a button in the sidebar and update the page selection on click
for page, label in pages.items():
    if st.sidebar.button(label, key=page):
        st.session_state.page_selection = page

# Use the selected page from session state
page_selection = st.session_state.page_selection

# Display content based on the selected page
st.title(page_selection)  # This line shows the page title based on selection


st.title("Coffee Shop Sales Analysis")

# File uploader for CSV files
# uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# if uploaded_file is not None:
#     # Read the uploaded CSV file
#     data = pd.read_csv(uploaded_file)

# data = pd.read_csv(uploaded_file)
# Temporary placeholder for the uploaded file - Update path as required
data = pd.read_csv('F:\CoU_IT\Coffee_Shop_Sales.csv')

# Calculate Revenue after loading the data
if 'transaction_qty' in data.columns and 'unit_price' in data.columns:
    data['Revenue'] = data['transaction_qty'] * data['unit_price']
else:
    st.write("Error: The dataset does not contain 'transaction_qty' and/or 'unit_price' columns, required for Revenue calculation.")

# Display data preview
# st.write("Data Preview:", data.head())

# Convert transaction_date to datetime format if it's in the dataset
if 'transaction_date' in data.columns:
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])





# If "Home" page is selected
if page_selection == "Home":
    # Sidebar filters
    st.sidebar.header("Filter Options")

    # Date Range Filter
    if 'transaction_date' in data.columns:
        min_date = data['transaction_date'].min()
        max_date = data['transaction_date'].max()
        date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
        data = data[(data['transaction_date'] >= pd.to_datetime(date_range[0])) & (data['transaction_date'] <= pd.to_datetime(date_range[1]))]

    # Product Category Filter
    if 'product_category' in data.columns:
        categories = data['product_category'].unique().tolist()
        selected_categories = st.sidebar.multiselect("Select Product Categories", categories, default=categories)
        data = data[data['product_category'].isin(selected_categories)]

    # Product Type Filter
    if 'product_type' in data.columns:
        product_types = data['product_type'].unique().tolist()
        selected_product_types = st.sidebar.multiselect("Select Product Types", product_types, default=product_types)
        data = data[data['product_type'].isin(selected_product_types)]

    # Store Filter
    if 'store_id' in data.columns:
        stores = sorted(data['store_id'].unique())
        selected_stores = st.sidebar.multiselect("Select Stores", stores, default=stores)
        data = data[data['store_id'].isin(selected_stores)]

    # Price Range Filter
    if 'unit_price' in data.columns:
        min_price = float(data['unit_price'].min())
        max_price = float(data['unit_price'].max())
        price_range = st.sidebar.slider("Select Price Range", min_price, max_price, (min_price, max_price))
        data = data[(data['unit_price'] >= price_range[0]) & (data['unit_price'] <= price_range[1])]

    # Transaction Quantity Filter
    if 'transaction_qty' in data.columns:
        min_qty = int(data['transaction_qty'].min())
        max_qty = int(data['transaction_qty'].max())
        qty_range = st.sidebar.slider("Select Quantity Range", min_qty, max_qty, (min_qty, max_qty))
        data = data[(data['transaction_qty'] >= qty_range[0]) & (data['transaction_qty'] <= qty_range[1])]

    # Product Detail Search Filter
    if 'product_detail' in data.columns:
        product_search = st.sidebar.text_input("Search Product Details")
        if product_search:
            data = data[data['product_detail'].str.contains(product_search, case=False, na=False)]

    # Display main analysis
    st.subheader("Comprehensive Sales Analysis")
    #tough
        # Basic and Trendy Analysis Summary
    st.subheader("Key Sales Metrics")

    # Calculate basic metrics
    total_revenue = data['Revenue'].sum() if 'Revenue' in data.columns else data['transaction_qty'].sum() * data['unit_price'].mean()
    total_sales_volume = data['transaction_qty'].sum()
    top_category = data.groupby('product_category')['transaction_qty'].sum().idxmax()
    top_store = data.groupby('store_id')['transaction_qty'].sum().idxmax()

    # Create pie charts for each metric
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

    with col1:
        fig_total_revenue = go.Figure(go.Indicator(
            mode="number+delta",
            value=total_revenue,
            title={"text": "Total Revenue"},
            number={'prefix': "$"},
            delta={'reference': total_revenue * 0.9, 'relative': True, 'position': "top"}
        ))
        fig_total_revenue.update_layout(height=200, margin=dict(t=0, b=0))
        st.plotly_chart(fig_total_revenue, use_container_width=True)

    with col2:
        fig_total_volume = go.Figure(go.Indicator(
            mode="number+delta",
            value=total_sales_volume,
            title={"text": "Total Sales Volume"},
            delta={'reference': total_sales_volume * 0.9, 'relative': True, 'position': "top"}
        ))
        fig_total_volume.update_layout(height=200, margin=dict(t=0, b=0))
        st.plotly_chart(fig_total_volume, use_container_width=True)

    with col3:
        fig_top_category = go.Figure(go.Pie(
            labels=[top_category, "Other Categories"],
            values=[data[data['product_category'] == top_category]['transaction_qty'].sum(), total_sales_volume - data[data['product_category'] == top_category]['transaction_qty'].sum()],
            hole=0.5
        ))
        #fig_top_category.update_layout(title="Top Product Category", height=200, margin=dict(l=20, r=20, t=20, b=20))
        fig_top_category.update_layout(
        title={"text": "Top Product Category", "font_size": 16},
        height=200,
        font=dict(size=12),  # Decrease overall font size in pie chart
        margin=dict(t=30, b=10, l=10, r=10)  # Adjust margin to fit within the column
    )
        st.plotly_chart(fig_top_category, use_container_width=True)

    with col4:
        fig_top_store = go.Figure(go.Pie(
            labels=[top_store, "Other Stores"],
            values=[data[data['store_id'] == top_store]['transaction_qty'].sum(), total_sales_volume - data[data['store_id'] == top_store]['transaction_qty'].sum()],
            hole=0.5
        ))
        #fig_top_store.update_layout(title="Top Store by Sales Volume", height=200, margin=dict(l=20, r=20, t=20, b=20))
        fig_top_store.update_layout(
        title={"text": "Top Store by Sales<br>Volume", "font_size": 16},
        height=200,
        margin=dict(t=30, b=10, l=10, r=10)  # Adjust margin to fit within the column
    )
        st.plotly_chart(fig_top_store, use_container_width=True)
        
    # Top 10 Products Bar Chart
    if 'product_detail' in data.columns and 'transaction_qty' in data.columns:
        top_products = data.groupby('product_detail')['transaction_qty'].sum().nlargest(10)
        bold_colors = ['#ff5733', '#33c9ff', '#ff33a1', '#75ff33', '#ffdb33', '#6a33ff', '#ff3333', '#33ff57', '#338aff', '#ffa733']
        
        fig_bar = px.bar(
            top_products,
            x=top_products.index,
            y=top_products.values,
            title="Top 10 Products",
            labels={'x': 'Product', 'y': 'Quantity Sold'},
            color_discrete_sequence=bold_colors
        )
        fig_bar.update_layout(
            title={'x': 0.5},
            xaxis_title="Product",
            yaxis_title="Quantity Sold",
            margin=dict(r=50)
        )

    # Product Category Distribution Pie Chart
    if 'product_category' in data.columns:
        product_category_counts = data['product_category'].value_counts()
        
        fig_pie = px.pie(
            product_category_counts,
            values=product_category_counts.values,
            names=product_category_counts.index,
            title="Product Categories Distribute",
            color_discrete_sequence=['#ff6f61', '#6b5b95', '#88b04b', '#f7cac9', '#92a8d1', '#ff7f50', '#45b8ac', '#d5a6bd', '#e94b3c']
        )
        
        fig_pie.update_layout(
            title_font_size=24,
            font_size=18,
            legend_title_font_size=15,
            margin=dict(l=60)
        )

    # Mean, Median, and Mode for Daily Sales Volume
    if 'transaction_date' in data.columns:
        daily_sales = data.groupby(data['transaction_date'].dt.date).size()
        avg_daily_sales = daily_sales.mean()
        median_daily_sales = daily_sales.median()
        mode_daily_sales = daily_sales.mode()[0]  # Get the first mode if multiple modes

        fig_pie_stats = go.Figure(data=[go.Pie(
            labels=['Mean', 'Median', 'Mode'],
            values=[avg_daily_sales, median_daily_sales, mode_daily_sales],
            marker_colors=['#ff6b6b', '#4d79ff', '#f7b731']
        )])
        fig_pie_stats.update_layout(
            title="Mean, Median, Mode for<br> Daily Sales Volume",
            title_font_size=24,
            font_size=18
        )

    # Display the main charts side by side
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
        st.plotly_chart(fig_pie_stats, use_container_width=True)
    with col2:
        st.plotly_chart(fig_pie, use_container_width=True)


        # Additional Product Analysis - Popular Categories and Types
        st.subheader("Product Analysis - Popular Categories and Types")
        
        # Popular Product Categories
        category_sales = data.groupby('product_category')['transaction_qty'].sum().reset_index()
        fig_category_sales = px.bar(
            category_sales, x='product_category', y='transaction_qty',
            title="Total Sales by Product Category",
            labels={'product_category': 'Product Category', 'transaction_qty': 'Total Sales Quantity'},
            color='product_category',
            color_discrete_sequence=['#d9534f', '#5bc0de', '#5cb85c', '#f0ad4e', '#e74c3c', '#8e44ad', '#2ecc71', '#3498db', '#9b59b6']
        )
        st.plotly_chart(fig_category_sales, use_container_width=True)

        # Define a function to generate plots for each category
        def plot_category_type_sales(category_name):
            category_data = data[data['product_category'] == category_name]
            type_sales = category_data.groupby('product_type')['transaction_qty'].sum().reset_index()
            fig = px.bar(
                type_sales, x='product_type', y='transaction_qty',
                title=f"Popular Types within {category_name}",
                labels={'product_type': f"{category_name} Type", 'transaction_qty': 'Total Sales Quantity'},
                color='product_type',
                color_discrete_sequence=px.colors.qualitative.Bold  # Use a bold color palette for distinct colors
            )
            return fig

                # Group the data by store location and product, summing the transaction quantities
    location_sales = data.groupby(['store_location', 'product_detail'])['transaction_qty'].sum().unstack().fillna(0)

    # Loop through each store location and create a separate pie chart for each
    for store in location_sales.index:
        store_data = location_sales.loc[store]
        
        # Create a pie chart for each store location
        plt.figure(figsize=(8, 8))
        store_data.plot(kind='pie', autopct='%1.1f%%', startangle=90, title=f"Sales Distribution by Product at {store} Store Location")
        
        # Set labels and title
        plt.ylabel("")  # Remove the y-axis label for a cleaner look
        plt.legend(title="Product Detail", bbox_to_anchor=(1.05, 1), loc='upper left')

        # Display the plot
        plt.show()

    


        # Display plots for each category side by side
        

        categories = ["Packaged Chocolate", "Loose Tea", "Coffee beans", "Branded", "Coffee", 
              "Tea", "Bakery", "Drinking Chocolate", "Flavours"]

# Display plots for each category in a row-by-row structure
        num_columns = 3  # Number of columns to display in a row

# Use a loop to go through each category and plot it only once
    for idx, category in enumerate(categories):
        col_idx = idx % num_columns
        if col_idx == 0:
            cols = st.columns(num_columns)  # Create a new row for every set of 3

        with cols[col_idx]:
            unique_key = f"chart_{category}_{idx}"  # Ensure each plot has a unique key
            st.plotly_chart(plot_category_type_sales(category), use_container_width=True, key=unique_key)





# Level 1 Analysis Section
elif page_selection == "Level 1":
    st.subheader("Level 1 Analysis: Revenue Analysis")

    # 3. Z-Score Calculation for Purchase Amount
    data['z_score_purchase'] = (data['transaction_qty'] - data['transaction_qty'].mean()) / data['transaction_qty'].std()
    fig_hist = px.histogram(
        data, x='z_score_purchase', nbins=20, title="Z-Score Distribution<br> for Transaction Quantities",
        color_discrete_sequence=['#66c2a5']
    )
    fig_hist.add_vline(x=0, line_dash="dash", line_color="red")

    # 4. Top 3 Most Sold Product Categories by Revenue in a Pie Chart
    data['revenue'] = data['transaction_qty'] * data['unit_price']
    top_categories = data.groupby('product_category').agg(
        total_qty=('transaction_qty', 'sum'),
        total_revenue=('revenue', 'sum')
    ).sort_values(by='total_qty', ascending=False).head(3)
    fig_category_pie = px.pie(
        top_categories, values='total_revenue', names=top_categories.index,
        title="Top 3 Product Categories<br> by Revenue",
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    # 5. Comparison of Variance and Standard Deviation
    variance = data['transaction_qty'].var()
    std_dev = data['transaction_qty'].std()
    fig_var_std = go.Figure(data=[
        go.Bar(name="Variance", x=["Variance"], y=[variance], marker_color='#a6cee3'),
        go.Bar(name="Standard Deviation", x=["Standard Deviation"], y=[std_dev], marker_color='#1f78b4')
    ])
    fig_var_std.update_layout(barmode='group', title="Comparison of Variance and<br> Standard Deviation")

    # Display the first three figures side by side
    col1, col2, col3 = st.columns(3)
    with col1:
        st.plotly_chart(fig_hist, use_container_width=True)
    with col2:
        st.plotly_chart(fig_category_pie, use_container_width=True)
    with col3:
        st.plotly_chart(fig_var_std, use_container_width=True)

    # --- Sequential Graphs Below ---

    # Total Revenue by Product Category
    category_revenue = data.groupby('product_category').agg({'revenue': 'sum'}).reset_index()
    if not category_revenue.empty:
        st.subheader("Total Revenue by Product Category")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=category_revenue, x='revenue', y='product_category', palette='viridis', ax=ax1)
        ax1.set_title('Total Revenue by Product Category')
        ax1.set_xlabel('Revenue')
        ax1.set_ylabel('Category')
        st.pyplot(fig1)

    # Top 10 Products by Revenue
    top_products = data.groupby('product_detail').agg({'revenue': 'sum'}).nlargest(10, 'revenue').reset_index()
    if not top_products.empty:
        st.subheader("Top 10 Products by Revenue")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.barplot(data=top_products, x='revenue', y='product_detail', palette='coolwarm', ax=ax2)
        ax2.set_title('Top 10 Products by Revenue')
        ax2.set_xlabel('Revenue')
        ax2.set_ylabel('Product')
        st.pyplot(fig2)

    # Average Transaction Quantity by Store Location
    store_avg_qty = data.groupby('store_location')['transaction_qty'].mean()
    st.subheader("Average Transaction Quantity per Store Location")
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=store_avg_qty.index, y=store_avg_qty.values, palette='crest', ax=ax4)
    ax4.set_title("Average Transaction Quantity per Store Location")
    ax4.set_xlabel("Store Location")
    ax4.set_ylabel("Average Transaction Quantity")
    st.pyplot(fig4)

    # Total Sales per Store Location as a Percentage
    location_sales = data.groupby('store_location')['transaction_qty'].sum()
    location_sales_percentage = (location_sales / location_sales.sum()) * 100
    st.write("Percentage of Total Sales by Store Location:")
    st.write(location_sales_percentage)
    st.subheader("Percentage of Total Sales by Store Location")
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    location_sales_percentage.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax5, cmap='Set3')
    ax5.set_ylabel("")
    ax5.set_title("Percentage of Total Sales by Store Location")
    st.pyplot(fig5)

    # Average Daily Unique Products per Store Location
    unique_products_daily = data.groupby(['transaction_date', 'store_location'])['product_id'].nunique()
    avg_unique_products = unique_products_daily.groupby('store_location').mean()
    st.subheader("Average Daily Unique Products per Store Location")
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=avg_unique_products.index, y=avg_unique_products.values, palette='Spectral', ax=ax6)
    ax6.set_title("Average Daily Unique Products per Store Location")
    ax6.set_xlabel("Store Location")
    ax6.set_ylabel("Average Daily Unique Products")
    st.pyplot(fig6)

    # Average Transaction Value per Store Location
    data['transaction_value'] = data['transaction_qty'] * data['unit_price']
    avg_transaction_value = data.groupby('store_location')['transaction_value'].mean()
    st.write("Average Transaction Value per Store Location:")
    st.write(avg_transaction_value)
    st.subheader("Average Transaction Value per Store Location")
    fig7, ax7 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=avg_transaction_value.index, y=avg_transaction_value.values, palette='cool', ax=ax7)
    ax7.set_title("Average Transaction Value per Store Location")
    ax7.set_xlabel("Store Location")
    ax7.set_ylabel("Average Transaction Value ($)")
    st.pyplot(fig7)

    # Sales Volume by Hour with Peak Hour Analysis
    data['transaction_datetime'] = pd.to_datetime(
        data['transaction_date'].astype(str) + ' ' + data['transaction_time'], errors='coerce'
    )
    data = data.dropna(subset=['transaction_datetime'])
    data['transaction_hour'] = data['transaction_datetime'].dt.hour
    hourly_sales = data.groupby('transaction_hour')['transaction_qty'].sum()
    peak_hour = hourly_sales.idxmax()
    st.write("Peak Hour of Sales:", peak_hour)
    st.write(hourly_sales)
    st.subheader("Sales Volume by Hour")
    fig8, ax8 = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=hourly_sales.index, y=hourly_sales.values, ax=ax8)
    ax8.axvline(peak_hour, color='red', linestyle='--', label='Peak Hour')
    ax8.legend()
    ax8.set_title("Sales Volume by Hour")
    ax8.set_xlabel("Hour of the Day")
    ax8.set_ylabel("Sales Volume")
    st.pyplot(fig8)

    # Top Products Purchased During Peak Hour
    peak_hour_data = data[data['transaction_hour'] == peak_hour]
    product_sales_peak_hour = peak_hour_data['product_category'].value_counts().head(10)
    st.write("Top Products Purchased During Peak Hour:")
    st.write(product_sales_peak_hour)
    st.subheader("Top Products Purchased During Peak Hour")
    fig9, ax9 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=product_sales_peak_hour.index, y=product_sales_peak_hour.values, palette='plasma', ax=ax9)
    ax9.set_title("Top Products Purchased During Peak Hour")
    ax9.set_xlabel("Product Category")
    ax9.set_ylabel("Number of Transactions")
    st.pyplot(fig9)


# elif page_selection == "Level 2":
#         st.subheader("Level 2 Analysis: In-Depth Sales Insights")
#         st.write("Further analysis for Level 2 can be added here.")
elif page_selection == "Level 2":
    st.subheader("Level 2 Analysis: In-Depth Sales Insights")

    # Days and Times of the Week with the Highest Sales Volume
    st.write("### Days and Times of the Week with the Highest Sales Volume")
    # Ensure 'transaction_date' and 'transaction_time' are in datetime format
    data['transaction_date'] = pd.to_datetime(data['transaction_date'], errors='coerce')
    data['transaction_time'] = pd.to_datetime(data['transaction_time'], format='%H:%M:%S', errors='coerce')

    # Extract day of the week and hour
    data['day_of_week'] = data['transaction_date'].dt.day_name()
    data['hour'] = data['transaction_time'].dt.hour

    # Group by day and hour to get sales volume
    day_hour_sales = data.groupby(['day_of_week', 'hour'])['transaction_qty'].sum().unstack().fillna(0)

    # Sort days for consistency in display (Monday to Sunday)
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_hour_sales = day_hour_sales.reindex(day_order)

    # Create an interactive heatmap
    fig_heatmap = px.imshow(
        day_hour_sales,
        labels=dict(x="Hour", y="Day of the Week", color="Sales Volume"),
        x=day_hour_sales.columns,
        y=day_hour_sales.index,
        color_continuous_scale="YlGnBu",
        aspect="auto",
        title="Sales Volume by Day of Week and Hour"
    )
    fig_heatmap.update_layout(margin=dict(l=60, r=60, t=40, b=40))
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Average Unit Price Across Product Categories
    st.write("### Average Unit Price Across Product Categories")
    avg_unit_price_by_category = data.groupby('product_category')['unit_price'].mean().reset_index()

    # Create an interactive bar chart
    fig_bar_avg_price = px.bar(
        avg_unit_price_by_category,
        x='product_category',
        y='unit_price',
        title="Average Unit Price by Product Category",
        labels={'unit_price': 'Average Unit Price ($)', 'product_category': 'Product Category'},
        color='product_category',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_bar_avg_price.update_layout(xaxis_tickangle=-45, margin=dict(l=60, r=60, t=40, b=80))
    st.plotly_chart(fig_bar_avg_price, use_container_width=True)

    # Correlation Between Transaction Quantity and Unit Price
    st.write("### Correlation Between Transaction Quantity and Unit Price")
    correlation = data['transaction_qty'].corr(data['unit_price'])
    st.write(f"Correlation between Transaction Quantity and Unit Price: {correlation:.2f}")

    # Scatter plot for correlation
    fig_scatter_corr = px.scatter(
        data,
        x='transaction_qty',
        y='unit_price',
        trendline="ols",
        title="Correlation Between Transaction Quantity and Unit Price",
        labels={'transaction_qty': 'Transaction Quantity', 'unit_price': 'Unit Price ($)'},
        opacity=0.6
    )
    fig_scatter_corr.update_traces(marker=dict(color='#1f77b4'))
    fig_scatter_corr.update_layout(margin=dict(l=60, r=60, t=40, b=40))
    st.plotly_chart(fig_scatter_corr, use_container_width=True)

     
     #hree
        # Sidebar filters
    st.sidebar.header("Filter Sales Growth Analysis")
    selected_location = st.sidebar.selectbox("Select Store Location", options=data['store_location'].unique())
    start_date = st.sidebar.date_input("Start Date", value=data['transaction_date'].min())
    end_date = st.sidebar.date_input("End Date", value=data['transaction_date'].max())

    # Filter data by selected location and date range
    filtered_data = data[
        (data['store_location'] == selected_location) &
        (data['transaction_date'] >= pd.to_datetime(start_date)) &
        (data['transaction_date'] <= pd.to_datetime(end_date))
    ]

    # Calculate daily sales growth for filtered data
    daily_sales = filtered_data.groupby(['store_location', 'transaction_date'])['transaction_qty'].sum().reset_index()
    daily_sales['sales_growth'] = daily_sales.groupby('store_location')['transaction_qty'].diff()
    store_sales_growth = daily_sales.groupby('store_location')['sales_growth'].sum().sort_values(ascending=False)

    st.subheader("Store Location Sales Growth Over the Period")
    st.write(f"Sales Growth for {selected_location} from {start_date} to {end_date}")
    st.write(store_sales_growth)

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=store_sales_growth.index, y=store_sales_growth.values, ax=ax)
    ax.set_title(f"Sales Growth for {selected_location} from {start_date} to {end_date}")
    ax.set_xlabel("Store Location")
    ax.set_ylabel("Total Sales Growth")
    st.pyplot(fig)
    
    #huu
        # Sidebar filter to select the number of top categories to display
    st.sidebar.header("Top Product Categories by Store Location")
    selected_location = st.sidebar.selectbox("Select Store Location", options=data['store_location'].unique(), key="location_selection")
    top_n = st.sidebar.slider("Number of Top Categories to Display", min_value=1, max_value=5, value=3)

    # Calculate sales volume by product category and store location
    location_category_sales = data.groupby(['store_location', 'product_category'])['transaction_qty'].sum().reset_index()

    # Get top N categories for each location
    top_categories_each_location = location_category_sales.groupby('store_location').apply(
        lambda x: x.nlargest(top_n, 'transaction_qty')
    ).reset_index(drop=True)

    # Filter for the selected location
    filtered_categories = top_categories_each_location[top_categories_each_location['store_location'] == selected_location]

    # Display data
    st.subheader(f"Top {top_n} Product Categories in {selected_location}")
    st.write(filtered_categories)

    # Visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x='product_category', y='transaction_qty', data=filtered_categories, ax=ax
    )
    ax.set_title(f"Top {top_n} Product Categories in {selected_location}")
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Sales Volume")
    st.pyplot(fig)
    #extra


    # Set up Streamlit rows for side-by-side display of two charts per row
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # 1. Daily Sales Trend
    with row1_col1:
        # Calculate daily sales volume
        daily_sales_trend = data.groupby('transaction_date')['transaction_qty'].sum().reset_index()

        # Interactive Altair chart for daily sales
        st.write("### Daily Sales Trend")
        daily_sales_chart = alt.Chart(daily_sales_trend).mark_line().encode(
            x=alt.X('transaction_date:T', title='Date'),
            y=alt.Y('transaction_qty:Q', title='Sales Volume'),
            tooltip=['transaction_date', 'transaction_qty']
        ).properties(width=300, height=300, title="Daily Sales Volume")

        st.altair_chart(daily_sales_chart.interactive())

    # 2. Monthly Sales Trend
    with row1_col2:
        # Convert to month-year format and calculate monthly sales volume
        data['transaction_month'] = pd.to_datetime(data['transaction_date']).dt.to_period('M').astype(str)
        monthly_sales_trend = data.groupby('transaction_month')['transaction_qty'].sum().reset_index()

        # Interactive Altair chart for monthly sales
        st.write("### Monthly Sales Trend")
        monthly_sales_chart = alt.Chart(monthly_sales_trend).mark_line().encode(
            x=alt.X('transaction_month:T', title='Month'),
            y=alt.Y('transaction_qty:Q', title='Sales Volume'),
            tooltip=['transaction_month', 'transaction_qty']
        ).properties(width=300, height=300, title="Monthly Sales Volume")

        st.altair_chart(monthly_sales_chart.interactive())

    # 3. Sales by Product Category
    with row2_col1:
        # Calculate total sales volume by product category
        category_sales_trend = data.groupby('product_category')['transaction_qty'].sum().reset_index()

        # Interactive Altair chart for product category sales
        st.write("### Sales by Product Category")
        category_sales_chart = alt.Chart(category_sales_trend).mark_bar().encode(
            x=alt.X('product_category:N', title='Product Category'),
            y=alt.Y('transaction_qty:Q', title='Sales Volume'),
            tooltip=['product_category', 'transaction_qty']
        ).properties(width=300, height=300, title="Sales Volume by Product Category")

        st.altair_chart(category_sales_chart.interactive())

    # 4. Average Sales Price Trend
    with row2_col2:
        # Calculate daily average sales price
        data['sales_value'] = data['transaction_qty'] * data['unit_price']
        avg_price_trend = data.groupby('transaction_date')['sales_value'].sum() / data.groupby('transaction_date')['transaction_qty'].sum()
        avg_price_trend = avg_price_trend.reset_index(name='avg_sales_price')

        # Interactive Altair chart for average sales price trend
        st.write("### Average Sales Price Trend")
        avg_price_chart = alt.Chart(avg_price_trend).mark_line().encode(
            x=alt.X('transaction_date:T', title='Date'),
            y=alt.Y('avg_sales_price:Q', title='Average Price ($)'),
            tooltip=['transaction_date', 'avg_sales_price']
        ).properties(width=300, height=300, title="Average Sales Price Over Time")

        st.altair_chart(avg_price_chart.interactive())

        

        



    

            

        

        
elif page_selection == "Level 3":
        st.subheader("Level 3 Analysis: Critical Thinking Insights")
        #st.write("Further analysis for Level 3 can be added here.")
       

        # Level 3: Critical Thinking Insights

        # 1. Top Factors Contributing to Higher Sales Volume in Specific Locations
        st.write("## Top Factors Contributing to Higher Sales Volume in Specific Locations")
        # Calculate sales volume by product type and location
        location_product_sales = data.groupby(['store_location', 'product_type'])['transaction_qty'].sum().reset_index()

        # Interactive bar chart by product type per location
        location_product_chart = alt.Chart(location_product_sales).mark_bar().encode(
            x=alt.X('store_location:N', title='Store Location'),
            y=alt.Y('transaction_qty:Q', title='Sales Volume'),
            color='product_type:N',
            tooltip=['store_location', 'product_type', 'transaction_qty']
        ).properties(width=600, height=400, title="Sales Volume by Product Type and Location")

        st.altair_chart(location_product_chart.interactive())
        st.write("**Insight**: Identify which product types are most popular in high-performing locations to determine key factors influencing sales. This insight can help in focusing product assortment and marketing efforts.")

        # 2. Impact of Time of Day on Sales of Specific Product Types
        st.write("## Impact of Time of Day on Sales of Specific Product Types")
        # Extract hour from transaction time
        data['transaction_hour'] = pd.to_datetime(data['transaction_time']).dt.hour
        hourly_sales = data.groupby(['transaction_hour', 'product_type'])['transaction_qty'].sum().reset_index()

        # Line chart for hourly sales by product type
        hourly_sales_chart = alt.Chart(hourly_sales).mark_line().encode(
            x=alt.X('transaction_hour:O', title='Hour of Day'),
            y=alt.Y('transaction_qty:Q', title='Sales Volume'),
            color='product_type:N',
            tooltip=['transaction_hour', 'product_type', 'transaction_qty']
        ).properties(width=600, height=400, title="Sales Volume by Hour for Product Types")

        st.altair_chart(hourly_sales_chart.interactive())
        st.write("**Insight**: Observe peak sales hours for products like coffee vs. tea. This can help in tailoring promotions or optimizing staffing based on demand throughout the day.")

        # 3. Product Category with Highest Potential for Price Increase Without Impacting Sales
        st.write("## Product Category with Highest Potential for Price Increase Without Impacting Sales")
        # Calculate total sales volume and average price per category
        category_price_volume = data.groupby('product_category').agg({'transaction_qty': 'sum', 'unit_price': 'mean'}).reset_index()

        # Scatter plot to compare average price and total sales volume
        price_volume_chart = alt.Chart(category_price_volume).mark_circle(size=100).encode(
            x=alt.X('unit_price:Q', title='Average Unit Price ($)'),
            y=alt.Y('transaction_qty:Q', title='Total Sales Volume'),
            color='product_category:N',
            tooltip=['product_category', 'transaction_qty', 'unit_price']
        ).properties(width=600, height=400, title="Sales Volume vs. Average Price by Product Category")

        st.altair_chart(price_volume_chart.interactive())
        st.write("**Insight**: Categories with high sales volume and lower average prices may tolerate a price increase, as long as demand remains steady.")

        # 4. Trends and Opportunities to Boost Sales in Underperforming Locations
        st.write("## Trends and Opportunities to Boost Sales in Underperforming Locations")
        # Calculate average sales by location
        average_sales_location = data.groupby('store_location')['transaction_qty'].mean().reset_index()

        # Bar chart of average sales by location
        underperforming_chart = alt.Chart(average_sales_location).mark_bar().encode(
            x=alt.X('store_location:N', title='Store Location'),
            y=alt.Y('transaction_qty:Q', title='Average Sales Volume'),
            tooltip=['store_location', 'transaction_qty']
        ).properties(width=600, height=400, title="Average Sales Volume by Location")

        st.altair_chart(underperforming_chart.interactive())
        st.write("**Insight**: Highlight trends in product popularity or timing in high-performing stores that could be adapted in underperforming locations to improve their sales.")

        # 5. Transaction Patterns on High-Traffic vs. Low-Traffic Days
        st.write("## Transaction Patterns on High-Traffic vs. Low-Traffic Days")
        # Define high-traffic and low-traffic days based on daily transaction volumes
        daily_transactions = data.groupby('transaction_date')['transaction_qty'].sum().reset_index()
        threshold = daily_transactions['transaction_qty'].median()
        high_traffic_days = daily_transactions[daily_transactions['transaction_qty'] > threshold]['transaction_date']
        low_traffic_days = daily_transactions[daily_transactions['transaction_qty'] <= threshold]['transaction_date']

        # Separate data based on high- and low-traffic days
        data['traffic_day'] = data['transaction_date'].apply(lambda x: 'High' if x in high_traffic_days.values else 'Low')
        traffic_sales = data.groupby(['traffic_day', 'product_type'])['transaction_qty'].sum().reset_index()

        # Bar chart of product sales on high vs. low-traffic days
        traffic_chart = alt.Chart(traffic_sales).mark_bar().encode(
            x=alt.X('traffic_day:N', title='Traffic Day Type'),
            y=alt.Y('transaction_qty:Q', title='Sales Volume'),
            color='product_type:N',
            tooltip=['traffic_day', 'product_type', 'transaction_qty']
        ).properties(width=600, height=400, title="Sales Volume on High- vs. Low-Traffic Days")

        st.altair_chart(traffic_chart.interactive())
        st.write("**Insight**: Identify products that consistently perform well on high- and low-traffic days for targeted promotions.")

        # 6. Store Location with Longest Peak Hour Duration
        st.write("## Store Location with Longest Peak Hour Duration")
        # Group by store location and transaction hour to find peak hours
        peak_hours = data.groupby(['store_location', 'transaction_hour'])['transaction_qty'].sum().reset_index()

        # Heatmap of transaction volume by store location and hour
        peak_hour_chart = alt.Chart(peak_hours).mark_rect().encode(
            x=alt.X('transaction_hour:O', title='Hour of Day'),
            y=alt.Y('store_location:N', title='Store Location'),
            color=alt.Color('transaction_qty:Q', title='Sales Volume'),
            tooltip=['store_location', 'transaction_hour', 'transaction_qty']
        ).properties(width=600, height=400, title="Peak Hours by Store Location")

        st.altair_chart(peak_hour_chart.interactive())
        st.write("**Insight**: Locations with extended peak hours may need optimized staffing, while others can benefit from targeted promotions during quieter times.")

        # 7. Reasons for Specific Store Location’s Higher Sales Volume
        st.write("## Reasons for Specific Store Location’s Higher Sales Volume")
        # Calculate sales volume by location and product variety (distinct products sold)
        location_product_variety = data.groupby('store_location').agg({'transaction_qty': 'sum', 'product_id': 'nunique'}).reset_index()
        location_product_variety = location_product_variety.rename(columns={'product_id': 'product_variety'})

        # Scatter plot of sales volume vs. product variety per location
        location_variety_chart = alt.Chart(location_product_variety).mark_circle(size=100).encode(
            x=alt.X('product_variety:Q', title='Product Variety'),
            y=alt.Y('transaction_qty:Q', title='Total Sales Volume'),
            color='store_location:N',
            tooltip=['store_location', 'transaction_qty', 'product_variety']
        ).properties(width=600, height=400, title="Sales Volume vs. Product Variety by Location")

        st.altair_chart(location_variety_chart.interactive())
        st.write("**Insight**: Locations offering a wider variety of products may attract higher sales, suggesting a potential to increase variety in low-performing stores.")

        # 8. Consistency of High Sales Performance Across Product Types
        st.write("## Consistency of High Sales Performance Across Product Types")
        # Calculate average sales by product type and store location
        location_type_sales = data.groupby(['store_location', 'product_type'])['transaction_qty'].mean().reset_index()

        # Heatmap of average sales by store and product type
        consistency_chart = alt.Chart(location_type_sales).mark_rect().encode(
            x=alt.X('product_type:N', title='Product Type'),
            y=alt.Y('store_location:N', title='Store Location'),
            color=alt.Color('transaction_qty:Q', title='Average Sales Volume'),
            tooltip=['store_location', 'product_type', 'transaction_qty']
        ).properties(width=600, height=400, title="Average Sales by Product Type and Store Location")

        st.altair_chart(consistency_chart.interactive())
        st.write("**Insight**: Locations that show consistent high performance across multiple product types may reveal best practices that can be applied to other stores.")


else:
    st.write("Please upload a CSV file to begin the analysis.")



