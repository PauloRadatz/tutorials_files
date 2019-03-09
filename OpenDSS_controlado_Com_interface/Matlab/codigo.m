
% Paulo Radatz

clc
clear all

% Initialize OpenDSS
% Create the OpenDSS Object
DSSobj = actxserver('OpenDSSEngine.DSS');

% Start up the solver

if ~DSSobj.Start(0),
    disp('Unable to start the OpenDSS Engine')
return
end

% Set up the interface variables
DSSText = DSSobj.Text;
DSSCircuit = DSSobj.ActiveCircuit;
DSSSolution = DSSCircuit.Solution;

% Run our OpenDSS file
DSSText.command = 'Compile (C:\Users\PauloRicardo\Desktop\TCC-Rede13\MASTER_RedeTeste13Barras.dss)';


LoadMult = 0.9;

Vmin = 1.0;

while Vmin > 0.95
    DSSSolution.LoadMult = LoadMult;
    DSSSolution.Solve;


    % Get bus voltage magnitudes in pu and distances from energy meter
    % Plot it in a scatter plot

    VA = DSSCircuit.AllNodeVmagPUByPhase(1);
    DistA = DSSCircuit.AllNodeDistancesByPhase(1);
    VB = DSSCircuit.AllNodeVmagPUByPhase(2);
    DistB = DSSCircuit.AllNodeDistancesByPhase(2);
    VC = DSSCircuit.AllNodeVmagPUByPhase(3);
    DistC = DSSCircuit.AllNodeDistancesByPhase(3);

    Vmin = min(VA);
    
    if Vmin > min(VB),
        Vmin = min(VB);
    end
    
    if Vmin > min(VC),
        Vmin = min(VC);
    end    
    
    maxX = max(DistA) + 0.1;

    if max(DistB) > maxX,
        maxX = max(DistB) + 0.1;
    end

    if max(DistC) > maxX,
        maxX = max(DistC) + 0.1;
    end



    % Make our plot

    figure

    plot(DistA, VA, 'k*');
    hold on;
    plot(DistB, VB, 'b+');
    hold on;
    plot(DistC, VC, 'gd');
    hold on;

    plot([0, maxX], [0.95, 0.95], 'r');
    plot([0, maxX], [1.05, 1.05], 'r');

    legend('Phase A','Phase B','Phase C');
    title(['Voltage Profile - LoadMult = ' num2str(DSSSolution.LoadMult)]);
    ylabel('Volts (pu)');
    xlabel('Distance From the EnergyMeter');

    grid on;

    ylim([0.9 1.1])
    xlim([0 maxX])

    hold off
    
    LoadMult = LoadMult + 0.05;
end














































