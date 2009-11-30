import FWCore.ParameterSet.Config as cms

process = cms.Process("ANA")

# Message logger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.extend(['SusyACSkimAnalysis'])
process.MessageLogger.cerr.default.limit = -1
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

#-- Geometry ------------------------------------------------------------------
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('STARTUP31X_V1::All')
process.load("Configuration.StandardSequences.MagneticField_cff")

#-- PAT standard config -------------------------------------------------------
process.load("PhysicsTools.PatAlgos.patSequences_cff")

#-- JES -----------------------------------------------------------------------
#process.load("JetMETCorrections.Configuration.L2L3Corrections_Summer09_cff")
#process.load("JetMETCorrections.Configuration.L2L3Corrections_Summer09_7TeV_cff")


#-- Tuning of Monte Carlo matching --------------------------------------------
# Also match with leptons of opposite charge
process.electronMatch.checkCharge = False
process.muonMatch.checkCharge     = False
process.tauMatch.checkCharge      = False

#from PhysicsTools.PatAlgos.tools.jetTools import *
#switchJECSet(process,newName='Winter09',oldName='Summer08Redigi') # change from old to Winter08

### Input / output ###

# Input file
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
#    'file:/afs/cern.ch/cms/PRS/top/cmssw-data/relval200-for-pat-testing/FullSimTTBar-2_2_X_2008-11-03-STARTUP_V7-AODSIM.100.root'
#    'file:/user/magass/LM1_RECO_CMSSW3.root'
    'file:/user/magass/HIGGS_RECO_1.root',
    'file:/user/magass/HIGGS_RECO_2.root',
    'file:/user/magass/HIGGS_RECO_3.root'
#        '/pnfs/physik.rwth-aachen.de/cms/store/user/ata/test/ata/ADD_150_450_1jet_Mf2p5_2n_GRW_10TeV/ADD_150_450_1jet_Mf2p5_2n_GRW_10TeV_RECO/bfb9b1ca5534929b93d8c7d7bdccf0e7/RECO_2.root'
#    'file:/opt/user/magass/wprime_mu.root'
#    'file:/opt/user/magass/UNFILE_RECO_76.root'
#    '/pnfs/physik.rwth-aachen.de/cms/store/mc/Summer08/QCDpt2200/GEN-SIM-RECO/IDEAL_V9_reco-v1/0003/340BCBD7-13FD-DD11-AFB3-003048C3E7AF.root'
#    '/pnfs/physik.rwth-aachen.de/cms/store/mc/Winter09/Wjets-madgraph/GEN-SIM-DIGI-RECO/IDEAL_V11_FastSim_v1/0043/B2B774A3-A7D3-DD11-A098-0011114FBAD4.root'
    ),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# this is just to satisfy the parser - NO PAT file is created !
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName       = cms.untracked.string('dummy.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    dropMetaData   = cms.untracked.string('DROPPED'),
    outputCommands = cms.untracked.vstring('drop *')
#                                           'keep *_BoostedHiggsSubjets_*_*',
#                                           'keep *_cleanLayer1Jets_*_*')
    )


process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('out.root')
                                   )

from PhysicsTools.PatAlgos.tools.jetTools import *
#switchJetCollection(process,
#                           cms.InputTag('sisCone5CaloJets'),
#                           doJTA=True,            # Run Jet-Track association & JetCharge
#                           doBTagging=True,       # Run b-tagging
#                           jetCorrLabel=('SC5','Calo'), # example jet correction name; set to None for no JEC
#                           doType1MET=True,       # recompute Type1MET using these jets
#                           genJetCollection=cms.InputTag("sisCone5GenJets"))
addJetCollection(process,
                 cms.InputTag('BoostedHiggsSubjets'), 'BHS',
                 doJTA            = False,
                 doBTagging       = True,
                 jetCorrLabel     = ('AK5','Calo'),
                 doType1MET       = False,
                 doJetID      = False,
                 genJetCollection = cms.InputTag("antikt5GenJets"))
switchJetCollection(process,
                           cms.InputTag('antikt5CaloJets'),
                           doJTA            = True,           # Run Jet-Track association & JetCharge
                           doBTagging       = True,           # Run b-tagging
                           jetCorrLabel     = ('AK5','Calo'), # jet correction name; set to None for no JEC
                           doType1MET       = True,           # recompute Type1MET using these jets
                           genJetCollection = cms.InputTag("antikt5GenJets"))

# Add latest HcalNoiseSummary
process.load("RecoMET.METProducers.hcalnoiseinfoproducer_cfi")
process.hcalnoise.refillRefVectors = True
process.hcalnoise.hcalNoiseRBXCollName = "hcalnoise" # This has changed in 33X

### Definition of all tags here
elecTag   = cms.InputTag("cleanLayer1Electrons")
jetTag    = cms.InputTag("cleanLayer1Jets")
muonTag   = cms.InputTag("cleanLayer1Muons")
metTag    = cms.InputTag("layer1METs")
genTag    = cms.InputTag("genParticles")
genJetTag = cms.InputTag("antikt5GenJets")
#genJetTag = cms.InputTag("sisCone5GenJets")
#genJetTag = cms.InputTag("iterativeCone5GenJets")
vtxTag    = cms.InputTag("offlinePrimaryVertices")

### Analysis configuration ###
process.ACSkimAnalysis = cms.EDFilter(
    "SusyACSkimAnalysis",

    is_MC      = cms.bool(True),  # set to 'False' for real Data !
    is_SHERPA  = cms.bool(False),  # set to 'True' if running on SHERPA
    do_fatjets = cms.bool(True),  # set to 'True' for fat jets
                                   # if 'True', include process.BoostedHiggsSubjets below

    # IMPORTANT for QCD ! ! !
    pthat_low  = cms.double(-1.),
    pthat_high = cms.double(-1.),

    jetTag    = jetTag,
    elecTag   = elecTag,
    muonTag   = muonTag,
    metTag    = metTag,
    genTag    = genTag,
    genJetTag = genJetTag,
    vtxTag    = vtxTag,

    muopt  = cms.double(0.),
    muoeta = cms.double(2.5),
    elept  = cms.double(10.),
    eleeta = cms.double(2.5),
    jetpt  = cms.double(10.),
    jeteta = cms.double(2.5),
    jetfem = cms.double(0.9),
    met    = cms.double(0.),
    nele   = cms.int32(0),
    nmuo   = cms.int32(0),
    njet   = cms.int32(0),

    correction = cms.string('abs'),   # abs
    flavour    = cms.string('glu'),   # glu

    btag       = cms.string('trackCountingHighEffBJetTags'),

)

from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTrigger( process )
process.patTriggerSequence.remove( process.patTriggerMatcher )
process.patTriggerEvent.patTriggerMatches  = ()

# Be Careful !!!
# process.patTrigger.processName = "HLT8E29"
# process.patTriggerEvent.processName = "HLT8E29"

from RecoJets.JetProducers.CaloJetParameters_cfi import CaloJetParameters
from RecoJets.JetProducers.AnomalousCellParameters_cfi import AnomalousCellParameters
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.BoostedHiggsParameters_cfi import BoostedHiggsParameters

# these are ignored, but required by VirtualJetProducer:
virtualjet_parameters = cms.PSet(jetAlgorithm=cms.string("SISCone"), rParam=cms.double(0.00001))


process.BoostedHiggsSubjets = cms.EDProducer("BoostedHiggsProducer",
    BoostedHiggsParameters,
    virtualjet_parameters,
    #this is required also for GenJets of PFJets:
    AnomalousCellParameters,
    CaloJetParameters
)

process.BoostedHiggsSubjets.jetSize       = cms.double(1.2)
process.BoostedHiggsSubjets.massThreshold = cms.double(0.667)
process.BoostedHiggsSubjets.rtyCut        = cms.double(0.3)
process.BoostedHiggsSubjets.ptMin         = cms.double(100.0)  # not JES corrected !!!
process.BoostedHiggsSubjets.nSubjets      = cms.int32(3)       # b bbar + radiation


from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
run33xOn31xMC(process,
                  jetSrc = cms.InputTag("antikt5CaloJets"),
                  jetIdTag = "antikt5" )

### Define the paths
process.p = cms.Path(
    process.BoostedHiggsSubjets*    # comment out if not needed
    process.hcalnoise*
    process.patDefaultSequence*
    process.patTrigger*
    process.patTriggerEvent*
    process.ACSkimAnalysis
    )
# process.e = cms.EndPath( process.out )

