<?xml version="1.0" encoding="UTF-8"?>
<!--
  IEC 61850 System Configuration Description (SCD)
  Musina 33/11 kV Municipal Substation — Brownfield Protection Review
  Scope: One bay example — F1 Hospital Feeder (SEL-351S)
  Generated: Python brownfield assessment, Project 3
  Standard: IEC 61850-6 Ed2.1

  Notes:
    - This SCD covers the SEL-351S on F1 which is already IEC 61850 capable
    - CDG-11 relays on F2-F4 have NO IEC 61850 capability (hardwired only)
    - Phase 1 upgrade: SEL-351S MMS reporting to SCADA over Ethernet
    - Phase 2 upgrade: new IEDs on F2-F4 added to this SCD
    - GOOSE control block: GoCB_F1_Trip publishes trip to bay controller
-->
<SCL xmlns="http://www.iec.ch/61850/2003/SCL"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     version="2007" revision="B">

  <Header id="MUSINA_33_11KV_SCD"
          version="1" revision="0"
          toolID="BrownfieldAssessmentPython_Project3"
          nameStructure="IEDName"/>

  <Substation name="MUSINA_33_11KV"
              desc="Musina Municipal 33/11 kV Substation — Limpopo">

    <VoltageLevel name="VL_33kV" desc="33 kV Incomer from Eskom Musina">
      <Voltage unit="V" multiplier="k">33</Voltage>
      <Bay name="Bay_Incomer_33kV" desc="33 kV Eskom Incomer Bay">
        <ConductingEquipment type="CBR" name="CB_33KV_INCOMER"
                             desc="33 kV Incomer Circuit Breaker">
          <Terminal name="T1"
                    connectivityNode="MUSINA_33_11KV/VL_33kV/Bay_Incomer_33kV/BB_33KV"/>
        </ConductingEquipment>
      </Bay>
    </VoltageLevel>

    <VoltageLevel name="VL_11kV" desc="11 kV Distribution — 4 outgoing feeders">
      <Voltage unit="V" multiplier="k">11</Voltage>

      <!-- F1 Hospital Feeder Bay — SEL-351S (IEC 61850 capable) -->
      <Bay name="Bay_F1_Hospital"
           desc="F1 Hospital + Water Treatment Plant — CRITICAL LOAD">
        <ConductingEquipment type="CBR" name="CB_F1"
                             desc="F1 Feeder Circuit Breaker">
          <Terminal name="T1"
                    connectivityNode="MUSINA_33_11KV/VL_11kV/Bay_F1_Hospital/BB_11KV"/>
        </ConductingEquipment>
      </Bay>

      <!-- F2-F4: CDG-11 relays — no IEC 61850, hardwired only, Phase 2 upgrade -->
      <Bay name="Bay_F2_CBD"          desc="F2 CBD + Border Post — CDG-11, Phase 2 upgrade"/>
      <Bay name="Bay_F3_Residential"  desc="F3 Residential SSEG — CDG-11, Phase 2 upgrade"/>
      <Bay name="Bay_F4_Industrial"   desc="F4 Industrial — CDG-11, Phase 2 upgrade"/>

    </VoltageLevel>
  </Substation>

  <!-- ═══════════════════════════════════════════════════════
       IED: SEL-351S on F1 — only IEC 61850 capable relay
       Functions: PTOC (OC), PDIS (directional I>>), RREC (reclose)
       ═══════════════════════════════════════════════════════ -->
  <IED name="SEL351S_F1"
       desc="SEL-351S Numeric Protection Relay — F1 Hospital Feeder"
       manufacturer="SEL" type="SEL-351S" configVersion="1">

    <Services>
      <GOOSE max="4" fixedOffs="false"/>
      <ReportSettings rptID="Dyn" datSet="Dyn" optFields="Dyn"
                      bufTime="Dyn" trgOps="Dyn" intgPd="Dyn"/>
      <LogSettings logEna="Dyn" trgOps="Dyn"/>
      <TimerActivatedControl/>
    </Services>

    <AccessPoint name="S1" desc="Station bus Ethernet port">
      <Server>

        <!-- Logical Device: Protection functions -->
        <LDevice inst="PROT" desc="Protection Functions — F1">

          <LN0 lnClass="LLN0" inst="" lnType="LLN0_SEL351S"
               desc="Logical node zero — GOOSE and MMS control">

            <!-- Dataset 1: Trip signals published via GOOSE -->
            <DataSet name="DS_TripGoose" desc="GOOSE trip dataset — F1">
              <FCDA ldInst="PROT" prefix="" lnClass="PTOC" lnInst="1"
                    doName="Op" daName="general" fc="ST"
                    desc="Phase overcurrent trip"/>
              <FCDA ldInst="PROT" prefix="" lnClass="PTOC" lnInst="2"
                    doName="Op" daName="general" fc="ST"
                    desc="Earth fault trip (SEF)"/>
              <FCDA ldInst="PROT" prefix="DIR" lnClass="PTOC" lnInst="1"
                    doName="Op" daName="general" fc="ST"
                    desc="Directional instantaneous trip (I>>)"/>
            </DataSet>

            <!-- Dataset 2: MMS reporting to SCADA -->
            <DataSet name="DS_SCADA_Report" desc="MMS report dataset">
              <FCDA ldInst="PROT" prefix="" lnClass="MMXU" lnInst="1"
                    doName="A" daName="phsA.cVal.mag.f" fc="MX"
                    desc="Phase A current measurement"/>
              <FCDA ldInst="PROT" prefix="" lnClass="MMXU" lnInst="1"
                    doName="A" daName="phsB.cVal.mag.f" fc="MX"
                    desc="Phase B current measurement"/>
              <FCDA ldInst="PROT" prefix="" lnClass="MMXU" lnInst="1"
                    doName="A" daName="phsC.cVal.mag.f" fc="MX"
                    desc="Phase C current measurement"/>
              <FCDA ldInst="PROT" prefix="" lnClass="PTOC" lnInst="1"
                    doName="Str" daName="general" fc="ST"
                    desc="Overcurrent start (pickup)"/>
            </DataSet>

            <!-- GOOSE Control Block: Trip publication -->
            <GSEControl name="GoCB_F1_Trip"
                        desc="GOOSE CB — F1 trip to bay controller"
                        type="GOOSE"
                        datSet="DS_TripGoose"
                        appID="MUSINA_F1_TRIP_GoCB"
                        fixedOffs="false"
                        confRev="1"/>

            <!-- MMS Report Control Block: to SCADA -->
            <ReportControl name="RCB_F1_SCADA"
                           desc="MMS report to municipal SCADA"
                           datSet="DS_SCADA_Report"
                           rptID="SEL351S_F1_PROT_RCB01"
                           confRev="1" buffered="true" bufTime="0"
                           intgPd="5000">
              <TrgOps dchg="true" qchg="true" dupd="false" period="true"/>
              <OptFields seqNum="true" timeStamp="true" dataSet="true"
                         reasonCode="true" dataRef="false" entryID="true"
                         configRef="true" bufOvfl="true"/>
            </ReportControl>

          </LN0>

          <!-- PTOC 1: Phase overcurrent IDMT (Very Inverse, TMS=0.075) -->
          <LN prefix="" lnClass="PTOC" inst="1" lnType="PTOC_VI_Type"
              desc="Phase overcurrent — VI curve, TMS=0.075, Is=225A"/>

          <!-- PTOC 2: Sensitive Earth Fault (SEF) -->
          <LN prefix="" lnClass="PTOC" inst="2" lnType="PTOC_SEF_Type"
              desc="Sensitive earth fault — Is=30A (10% of NER limit)"/>

          <!-- PTOC DIR1: Directional instantaneous (I>>) -->
          <LN prefix="DIR" lnClass="PTOC" inst="1" lnType="PTOC_INST_Type"
              desc="Directional I>> — 2437A, forward looking into F1"/>

          <!-- RREC: Auto-reclose (future — blocked pending anti-islanding study) -->
          <LN prefix="" lnClass="RREC" inst="1" lnType="RREC_Type"
              desc="Auto-reclose — BLOCKED pending SSEG anti-islanding compliance"/>

          <!-- MMXU: Measurement unit — current, voltage, power -->
          <LN prefix="" lnClass="MMXU" inst="1" lnType="MMXU_Type"
              desc="Feeder F1 measurements — published to SCADA via MMS"/>

        </LDevice>
      </Server>
    </AccessPoint>
  </IED>

  <!-- ═══════════════════════════════════════════════════════
       Communication: Station bus Ethernet
       ═══════════════════════════════════════════════════════ -->
  <Communication>
    <SubNetwork name="StationBus_Musina"
                desc="IEC 61850 Station Bus — 100Mbit managed Ethernet switch"
                type="8-MMS">

      <!-- SEL-351S F1 connection -->
      <ConnectedAP iedName="SEL351S_F1" apName="S1">
        <Address>
          <P type="IP">192.168.10.101</P>
          <P type="IP-SUBNET">255.255.255.0</P>
          <P type="IP-GATEWAY">192.168.10.1</P>
          <P type="MAC-Address">02-00-00-00-01-01</P>
          <P type="OSI-PSEL">00 00 00 01</P>
        </Address>

        <!-- GOOSE multicast address for F1 trip -->
        <GSE ldInst="PROT" cbName="GoCB_F1_Trip">
          <Address>
            <P type="MAC-Address">01-0C-CD-01-00-01</P>
            <P type="APPID">0x0001</P>
            <P type="VLAN-ID">0x000</P>
            <P type="VLAN-PRIORITY">4</P>
          </Address>
          <MinTime unit="ms" multiplier="1">2</MinTime>
          <MaxTime unit="ms" multiplier="1">1000</MaxTime>
        </GSE>

        <!-- MMS report server address -->
        <SMV ldInst="PROT" cbName="RCB_F1_SCADA">
          <Address>
            <P type="MAC-Address">01-0C-CD-04-00-01</P>
            <P type="APPID">0x4001</P>
            <P type="VLAN-ID">0x000</P>
            <P type="VLAN-PRIORITY">4</P>
          </Address>
        </SMV>
      </ConnectedAP>

      <!--
        F2-F4: CDG-11 relays have no IEC 61850 access point.
        These bays are connected via hardwired trip circuits only.
        Phase 2 upgrade will add ConnectedAP entries here for new IEDs.
      -->

    </SubNetwork>
  </Communication>

</SCL>
