document.getElementById('fileInput').addEventListener('change', function(e) {
      const file = e.target.files[0];
  
      if (file) {
          const reader = new FileReader();
  
          reader.onload = function(e) {
              const fileContent = e.target.result;
  
              // Gọi hàm xử lý dữ liệu với nội dung của tệp tin
              processData(fileContent);
          };
  
          reader.readAsText(file);
      }
  });
  
  function processData(data) {
      // Xử lý dữ liệu ở đây (ví dụ: chuyển đổi dữ liệu CSV thành dạng phù hợp cho biểu đồ)
      // Sau đó, vẽ biểu đồ bằng Plotly hoặc một thư viện trực quan hóa dữ liệu khác
      const chartData = processDataToChartData(data);
  
      // Vẽ biểu đồ bằng Plotly
      const chartContainer = document.getElementById('chartContainer');
      Plotly.newPlot(chartContainer, chartData);
  }
  
  function processDataToChartData(data) {
      // Xử lý dữ liệu và chuyển đổi thành định dạng dữ liệu phù hợp với biểu đồ
      // Ví dụ: bạn có thể sử dụng thư viện như d3.js hoặc chỉnh sửa dữ liệu trực tiếp
  
      // Trả về dữ liệu cho biểu đồ
      return chartData;
  }
  