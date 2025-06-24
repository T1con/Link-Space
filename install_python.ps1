# Script tự động kiểm tra và hướng dẫn cài đặt Python cho Link Space
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Link Space - Kiểm tra Python" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Kiểm tra Python
Write-Host "🔍 Đang kiểm tra Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python đã được cài đặt: $pythonVersion" -ForegroundColor Green
        $pythonInstalled = $true
    } else {
        throw "Python không tìm thấy"
    }
} catch {
    Write-Host "❌ Python chưa được cài đặt hoặc không có trong PATH" -ForegroundColor Red
    $pythonInstalled = $false
}

if (-not $pythonInstalled) {
    Write-Host ""
    Write-Host "📥 Hướng dẫn cài đặt Python:" -ForegroundColor Cyan
    Write-Host "1. Truy cập: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. Tải phiên bản Python mới nhất" -ForegroundColor White
    Write-Host "3. Chạy file cài đặt" -ForegroundColor White
    Write-Host "4. QUAN TRỌNG: Đánh dấu 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host "5. Chọn 'Install Now'" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Hoặc cài đặt từ Microsoft Store:" -ForegroundColor Cyan
    Write-Host "1. Mở Microsoft Store" -ForegroundColor White
    Write-Host "2. Tìm 'Python 3.11' hoặc 'Python 3.12'" -ForegroundColor White
    Write-Host "3. Cài đặt" -ForegroundColor White
    Write-Host ""
    Write-Host "🔄 Sau khi cài đặt, khởi động lại PowerShell và chạy lại script này" -ForegroundColor Yellow
    Read-Host "Nhấn Enter để thoát"
    exit
}

# Kiểm tra pip
Write-Host ""
Write-Host "🔍 Đang kiểm tra pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pip đã sẵn sàng: $pipVersion" -ForegroundColor Green
    } else {
        throw "pip không tìm thấy"
    }
} catch {
    Write-Host "❌ pip không tìm thấy. Vui lòng cài đặt lại Python" -ForegroundColor Red
    Read-Host "Nhấn Enter để thoát"
    exit
}

# Kiểm tra thư viện Flask
Write-Host ""
Write-Host "🔍 Đang kiểm tra Flask..." -ForegroundColor Yellow
try {
    python -c "import flask" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Flask đã được cài đặt" -ForegroundColor Green
        $flaskInstalled = $true
    } else {
        throw "Flask không tìm thấy"
    }
} catch {
    Write-Host "❌ Flask chưa được cài đặt" -ForegroundColor Red
    $flaskInstalled = $false
}

if (-not $flaskInstalled) {
    Write-Host ""
    Write-Host "📦 Đang cài đặt Flask và các thư viện cần thiết..." -ForegroundColor Yellow
    try {
        pip install -r requirements_mobile.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Cài đặt thành công!" -ForegroundColor Green
        } else {
            throw "Lỗi cài đặt"
        }
    } catch {
        Write-Host "❌ Lỗi cài đặt thư viện" -ForegroundColor Red
        Write-Host "💡 Thử chạy: pip install -r requirements_mobile.txt" -ForegroundColor Yellow
        Read-Host "Nhấn Enter để thoát"
        exit
    }
}

# Tạo thư mục cần thiết
Write-Host ""
Write-Host "📁 Đang tạo thư mục cần thiết..." -ForegroundColor Yellow
$directories = @("static", "static/avatars", "static/uploads", "data/uploads")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Tạo thư mục: $dir" -ForegroundColor Green
    }
}

# Copy dữ liệu avatar nếu có
if (Test-Path "data/avatars") {
    Write-Host "📋 Đang copy avatar..." -ForegroundColor Yellow
    Copy-Item "data/avatars/*" "static/avatars/" -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Copy avatar hoàn tất" -ForegroundColor Green
}

# Copy dữ liệu upload nếu có
if (Test-Path "data/uploads") {
    Write-Host "📋 Đang copy uploads..." -ForegroundColor Yellow
    Copy-Item "data/uploads/*" "static/uploads/" -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Copy uploads hoàn tất" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Tất cả đã sẵn sàng!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Khởi động ứng dụng web:" -ForegroundColor Cyan
Write-Host "1. Chạy: python mobile_app.py" -ForegroundColor White
Write-Host "2. Hoặc double-click file: run_mobile.bat" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Truy cập ứng dụng:" -ForegroundColor Cyan
Write-Host "- Máy tính: http://localhost:5000" -ForegroundColor White
Write-Host "- Điện thoại: http://[IP_MÁY_TÍNH]:5000" -ForegroundColor White
Write-Host ""
Write-Host "👤 Tài khoản mặc định:" -ForegroundColor Cyan
Write-Host "- Username: T1con" -ForegroundColor White
Write-Host "- Password: (để trống)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Bạn có muốn khởi động ứng dụng ngay bây giờ? (y/n)"
if ($choice -eq "y" -or $choice -eq "Y") {
    Write-Host ""
    Write-Host "🚀 Đang khởi động Link Space..." -ForegroundColor Green
    python mobile_app.py
} else {
    Write-Host "👋 Hẹn gặp lại!" -ForegroundColor Cyan
} 