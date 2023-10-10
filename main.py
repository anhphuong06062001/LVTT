from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
plt.switch_backend('agg')

app = Flask(__name__)

# Tiền xử lý dữ liệu
# Thống kê
def statistics_data(df):
    if df is None:
        return None

    summary_stats = df.describe() 
    
    return summary_stats

# Hàm tạo biểu đồ thứ nhất (line chart)
def create_line_chart(df):
    #print(df['NGAY'].dtype)
    df['THANG'] = pd.to_datetime(df['NGAY']).dt.month
    monthly_data = df.groupby('THANG')[['UP', 'DOWN']].sum()
    df.set_index('NGAY', inplace=True)

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_data.index, monthly_data['UP'], label='Lưu lượng UP', color='blue', marker='o')
    plt.plot(monthly_data.index, monthly_data['DOWN'], label='Lưu lượng DOWN', color='red', marker='o')
    plt.xlabel('Tháng')
    plt.ylabel('Lưu lượng')
    plt.title('Biểu đồ Lưu lượng UP và DOWN theo tháng')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Lưu biểu đồ vào một đối tượng BytesIO để sau này truyền vào HTML
    img1 = BytesIO()
    plt.savefig(img1, format="png")
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode()

    plt.close()
    print(df)
    return plot_url1

# Hàm tạo biểu đồ thứ hai (bar chart)
def create_bar_chart(df):
    df['NGAY_USE'] = pd.to_datetime(df['NGAY']).dt.day
    daily_data = df.groupby('NGAY_USE')[['UP', 'DOWN']].sum()
    df.set_index('NGAY', inplace=True)
    bar_width = 0.4

    plt.figure(figsize=(12, 6))
    plt.bar(daily_data.index, daily_data['UP'], width=bar_width, label='Lưu lượng UP', color='blue', alpha=0.7)
    plt.bar(daily_data.index + bar_width, daily_data['DOWN'], width=bar_width, label='Lưu lượng DOWN', color='red', alpha=0.7)
    plt.xlabel('Ngày')
    plt.ylabel('Lưu lượng')
    plt.title('Biểu đồ Lưu lượng UP và DOWN hàng ngày')
    plt.legend()
    plt.grid(True)

    # Lưu biểu đồ vào một đối tượng BytesIO để sau này truyền vào HTML
    img2 = BytesIO()
    plt.savefig(img2, format="png")
    img2.seek(0)
    plot_url2 = base64.b64encode(img2.getvalue()).decode()

    plt.close()

    return plot_url2

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Chưa có tệp nào được tải lên."
        file = request.files['file']
 
        if file.filename == '':
            return "Vui lòng chọn tệp để tải lên."
        # Đọc tệp CSV
        if file:
            df = pd.read_csv(file)
            df_copy = df.copy()
            statictis = statistics_data(df)
            table_html = statictis.to_html(classes='table table-bordered table-striped', index=False)

            plot_url1 = create_line_chart(df)
            plot_url2 = create_bar_chart(df_copy)
            #plot_url2=plot_url2
            return render_template('result.html', plot_url1=plot_url1, plot_url2=plot_url2, st=table_html)
            #return render_template('result.html', table=table_html)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
