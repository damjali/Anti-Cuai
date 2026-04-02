import React, { useState } from "react";
import "./landingPage.css";

type FeatureKey =
  | "scamLink"
  | "phishingEmail"
  | "bankNumber"
  | "phoneNumber"
  | "emailCheck"
  | "aiWarning"
  | "autoHighlight";

const LandingPage: React.FC = () => {
  const [features, setFeatures] = useState<Record<FeatureKey, boolean>>({
    scamLink: true,
    phishingEmail: true,
    bankNumber: true,
    phoneNumber: true,
    emailCheck: true,
    aiWarning: true,
    autoHighlight: true,
  });

  const toggleFeature = (key: FeatureKey) => {
    setFeatures((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  return (
    <div className="container">
      <h1 className="title">Anti-Cuai</h1>
      <p className="subtitle">Your Smart Local Scam Protection</p>

      <div className="checklist">
        <FeatureItem
          label="Scam Link Detection"
          active={features.scamLink}
          onClick={() => toggleFeature("scamLink")}
        />

        <FeatureItem
          label="Phishing Email Detection"
          active={features.phishingEmail}
          onClick={() => toggleFeature("phishingEmail")}
        />

        <FeatureItem
          label="Bank Number Scam Check (Semak Mule)"
          active={features.bankNumber}
          onClick={() => toggleFeature("bankNumber")}
        />

        <FeatureItem
          label="Phone Number Scam Check"
          active={features.phoneNumber}
          onClick={() => toggleFeature("phoneNumber")}
        />

        <FeatureItem
          label="Email Scam Check"
          active={features.emailCheck}
          onClick={() => toggleFeature("emailCheck")}
        />

        <FeatureItem
          label="AI Suspicious Content Warning"
          active={features.aiWarning}
          onClick={() => toggleFeature("aiWarning")}
        />

        <FeatureItem
          label="Auto Highlight Suspicious Text"
          active={features.autoHighlight}
          onClick={() => toggleFeature("autoHighlight")}
        />
      </div>

      <button className="saveBtn">Save Preferences</button>
    </div>
  );
};

type FeatureItemProps = {
  label: string;
  active: boolean;
  onClick: () => void;
};

const FeatureItem: React.FC<FeatureItemProps> = ({
  label,
  active,
  onClick,
}) => {
  return (
    <div className="featureItem" onClick={onClick}>
      <span>{label}</span>
      <div className={`toggle ${active ? "active" : ""}`}>
        <div className="circle" />
      </div>
    </div>
  );
};

export default LandingPage;