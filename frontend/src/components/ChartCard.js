import React from 'react';

const ChartCard = ({ title, children, subtitle }) => {
  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        {subtitle && <p className="text-sm text-slate-400 mt-1">{subtitle}</p>}
      </div>
      <div className="w-full h-80">
        {children}
      </div>
    </div>
  );
};

export default ChartCard;
