import React, { useRef, useState, useEffect } from 'react';
import { Camera, RefreshCw, CheckCircle, AlertCircle, Sparkles, Upload } from 'lucide-react';

interface WebcamCaptureProps {
  onCapture: (imageBase64: string) => void;
  actionButtonText?: string;
  isProcessing?: boolean;
}

export const WebcamCapture: React.FC<WebcamCaptureProps> = ({
  onCapture,
  actionButtonText = 'Chụp ảnh & Điểm danh',
  isProcessing = false,
}) => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [isFaceAligned, setIsFaceAligned] = useState<boolean>(true);

  // Khởi động Camera thiết bị
  const startCamera = async () => {
    try {
      setCameraError(null);
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user',
        },
        audio: false,
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err: any) {
      console.error('Camera access error:', err);
      setCameraError(
        'Không thể mở webcam hoặc quyền truy cập camera bị từ chối. Bạn có thể sử dụng ảnh tải lên thay thế.'
      );
    }
  };

  useEffect(() => {
    startCamera();
    return () => {
      // Dọn dẹp stream khi unmount
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  // Chụp ảnh từ khung hình video hiện tại
  const captureFrame = () => {
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Flip canvas horizontally to match mirror preview
    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const base64 = canvas.toDataURL('image/jpeg', 0.92);
    setCapturedImage(base64);
  };

  const retakePhoto = () => {
    setCapturedImage(null);
    if (!stream) {
      startCamera();
    }
  };

  const handleConfirm = () => {
    if (capturedImage) {
      onCapture(capturedImage);
    }
  };

  // Hỗ trợ tải file ảnh nếu webcam không khả dụng
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result as string;
        setCapturedImage(base64);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="flex flex-col items-center w-full max-w-lg mx-auto">
      {/* Khung hiển thị Video / Canvas */}
      <div className="relative w-full aspect-4/3 bg-slate-900 rounded-3xl overflow-hidden border-2 border-slate-700 shadow-xl flex items-center justify-center">
        {capturedImage ? (
          // Khung ảnh đã chụp
          <img
            src={capturedImage}
            alt="Captured face"
            className="w-full h-full object-cover"
          />
        ) : (
          // Live Webcam Stream
          <>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover transform -scale-x-100"
            />

            {/* Face Oval Positioning Guide */}
            <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
              <div className="w-56 h-72 border-2 border-dashed border-sky-400/80 rounded-[50%] flex items-center justify-center shadow-[0_0_20px_rgba(56,189,248,0.2)]">
                {/* Scanning Laser Line */}
                <div className="w-full h-0.5 bg-gradient-to-r from-transparent via-cyan-400 to-transparent animate-pulse" />
              </div>
            </div>

            {/* HUD Status Bar */}
            <div className="absolute top-4 left-4 right-4 flex items-center justify-between text-xs text-white bg-slate-900/60 backdrop-blur-md px-3.5 py-2 rounded-xl">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping" />
                <span className="font-medium text-emerald-400">AI CAMERA LIVE</span>
              </div>
              <div className="flex items-center gap-1.5 text-slate-300">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                <span>InsightFace 512D</span>
              </div>
            </div>

            <div className="absolute bottom-4 inset-x-4 text-center">
              <span className="inline-block bg-slate-900/75 backdrop-blur-md text-slate-200 text-xs px-3.5 py-1.5 rounded-full font-medium shadow-md">
                Căn chỉnh khuôn mặt vào khung elip và giữ thẳng góc
              </span>
            </div>
          </>
        )}

        <canvas ref={canvasRef} className="hidden" />

        {/* Lỗi Camera */}
        {cameraError && !capturedImage && (
          <div className="absolute inset-0 bg-slate-900/90 p-6 flex flex-col items-center justify-center text-center text-white">
            <AlertCircle className="w-12 h-12 text-amber-400 mb-3" />
            <p className="text-sm text-slate-300 mb-4">{cameraError}</p>
            <label className="cursor-pointer px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-semibold flex items-center gap-2 transition-colors">
              <Upload className="w-4 h-4" />
              Tải ảnh chân dung từ máy tính
              <input type="file" accept="image/*" className="hidden" onChange={handleFileUpload} />
            </label>
          </div>
        )}
      </div>

      {/* Điều khiển Action Buttons */}
      <div className="mt-5 w-full flex items-center justify-center gap-3">
        {capturedImage ? (
          <>
            <button
              onClick={retakePhoto}
              disabled={isProcessing}
              className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-xl text-sm font-semibold flex items-center gap-2 transition-colors disabled:opacity-50"
            >
              <RefreshCw className="w-4 h-4" />
              Chụp lại
            </button>
            <button
              onClick={handleConfirm}
              disabled={isProcessing}
              className="flex-1 max-w-xs px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-sm font-bold flex items-center justify-center gap-2 shadow-lg shadow-blue-500/20 transition-all disabled:opacity-50"
            >
              {isProcessing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Đang xử lý AI...
                </>
              ) : (
                <>
                  <CheckCircle className="w-4 h-4" />
                  Xác nhận khuôn mặt
                </>
              )}
            </button>
          </>
        ) : (
          <button
            onClick={captureFrame}
            disabled={!!cameraError || isProcessing}
            className="w-full max-w-sm px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl text-sm font-bold flex items-center justify-center gap-2 shadow-lg shadow-blue-500/30 transition-all disabled:opacity-50"
          >
            <Camera className="w-5 h-5" />
            {actionButtonText}
          </button>
        )}
      </div>
    </div>
  );
};

export default WebcamCapture;
