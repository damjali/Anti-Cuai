import { useState, useEffect } from 'react';
import './App.css';

declare const chrome: any; 

function App() {
  // Master Toggles
  const [linkDetection, setLinkDetection] = useState(true);
  const [scamHighlight, setScamHighlight] = useState(true);

  // Sub-Toggles
  const [checkPhone, setCheckPhone] = useState(true);
  const [checkEmail, setCheckEmail] = useState(false); 
  const [checkBank, setCheckBank] = useState(true);

  // 1. LOAD: Fetch all settings from Chrome Storage on component mount
  useEffect(() => {
    if (typeof chrome !== 'undefined' && chrome.storage) {
      chrome.storage.local.get(
        ['linkDetection', 'scamHighlight', 'checkPhone', 'checkEmail', 'checkBank'], 
        (res: any) => {
          if (res.linkDetection !== undefined) setLinkDetection(res.linkDetection);
          if (res.scamHighlight !== undefined) setScamHighlight(res.scamHighlight);
          if (res.checkPhone !== undefined) setCheckPhone(res.checkPhone);
          if (res.checkEmail !== undefined) setCheckEmail(res.checkEmail);
          if (res.checkBank !== undefined) setCheckBank(res.checkBank);
        }
      );
    }
  }, []);

  // 2. SAVE: Automatically sync to Chrome Storage whenever any state changes
  useEffect(() => {
    if (typeof chrome !== 'undefined' && chrome.storage) {
      chrome.storage.local.set({
        linkDetection,
        scamHighlight,
        checkPhone,
        checkEmail,
        checkBank
      });
    }
  }, [linkDetection, scamHighlight, checkPhone, checkEmail, checkBank]);

  return (
    <div className="w-[350px] min-h-[450px] bg-[#12122b] flex flex-col font-sans text-white">
      
      {/* Header */}
      <div className="bg-[#1a1a2e] p-5 shadow-xl border-b border-[#2a2a4a]">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <span className="text-[#9a78ec]">🛡️</span> Anti-Cuai
        </h1>
        <p className="text-sm text-[#b0b0b0] mt-1">Active SemakMule Protection</p>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-5 flex flex-col gap-4">
        
        {/* Toggle 1: Link Detection */}
        <div className="bg-[#1a1a2e] p-4 rounded-xl shadow-lg border border-[#3e3e5c] flex justify-between items-center">
          <div>
            <h2 className="font-semibold text-white">Link Detection</h2>
            <p className="text-xs text-[#b0b0b0] mt-1">Scan DOM for phishing URLs</p>
          </div>
          <button 
            onClick={() => setLinkDetection(!linkDetection)}
            className={`w-12 h-6 rounded-full transition-colors relative flex items-center shadow-inner ${linkDetection ? 'bg-[#9a78ec]' : 'bg-[#3e3e5c]'}`}
          >
            <div className={`w-4 h-4 bg-[#e0e0e0] rounded-full absolute transition-transform shadow-md ${linkDetection ? 'translate-x-7' : 'translate-x-1'}`} />
          </button>
        </div>

        {/* Toggle 2: Master Scam Highlight */}
        <div className="bg-[#1a1a2e] p-4 rounded-xl shadow-lg border border-[#3e3e5c] flex flex-col">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="font-semibold text-white">Highlight Scams</h2>
              <p className="text-xs text-[#b0b0b0] mt-1">Crosscheck with SemakMule</p>
            </div>
            <button 
              onClick={() => setScamHighlight(!scamHighlight)}
              className={`w-12 h-6 rounded-full transition-colors relative flex items-center shadow-inner ${scamHighlight ? 'bg-[#9a78ec]' : 'bg-[#3e3e5c]'}`}
            >
              <div className={`w-4 h-4 bg-[#e0e0e0] rounded-full absolute transition-transform shadow-md ${scamHighlight ? 'translate-x-7' : 'translate-x-1'}`} />
            </button>
          </div>

          {/* Sub-Toggles Menu */}
          {scamHighlight && (
            <div className="mt-4 pt-4 border-t border-[#3e3e5c] flex flex-col gap-3">
              <p className="text-[10px] uppercase tracking-wider text-[#9a78ec] font-bold">What to scan:</p>
              
              <div className="flex justify-between items-center">
                <span className="text-sm text-[#d0d0d0]">📱 Phone Numbers</span>
                <input 
                  type="checkbox" 
                  checked={checkPhone} 
                  onChange={() => setCheckPhone(!checkPhone)}
                  className="accent-[#9a78ec] w-4 h-4 cursor-pointer"
                />
              </div>

              <div className="flex justify-between items-center">
                <span className="text-sm text-[#d0d0d0]">📧 Email Addresses</span>
                <input 
                  type="checkbox" 
                  checked={checkEmail} 
                  onChange={() => setCheckEmail(!checkEmail)}
                  className="accent-[#9a78ec] w-4 h-4 cursor-pointer"
                />
              </div>

              <div className="flex justify-between items-center">
                <span className="text-sm text-[#d0d0d0]">💳 Bank Accounts</span>
                <input 
                  type="checkbox" 
                  checked={checkBank} 
                  onChange={() => setCheckBank(!checkBank)}
                  className="accent-[#9a78ec] w-4 h-4 cursor-pointer"
                />
              </div>
            </div>
          )}
        </div>
        
        {/* Status Indicator */}
        <div className="mt-auto p-3 bg-[#103a10] border border-[#2d7d2d] rounded-lg">
          <p className="text-xs text-center text-[#88e088] font-medium">
            ✅ Extension is active and scanning
          </p>
        </div>

      </div>
    </div>
  );
}

export default App;