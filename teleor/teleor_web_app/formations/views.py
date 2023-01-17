from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from decimal import Decimal

@login_required
def index(request):
    formations = Formation.objects.all()
    branches = []
    for brancheItem in BrancheFormation.objects.all():
        branche = {
                "description" : brancheItem.description,
                "formations" : None if brancheItem.formations == None else brancheItem.formations.all()
                }
        branches.append(branche)
    return render(request, 'index/index.html', {
        "branches" : branches
    })

def calculateur_tarifs(formation, echeance, remise):
    remise = Decimal(remise)
    formule = echeance.code_echeance
    total = (formation.tarif_sans_acompte + formation.acompte) * (1 - remise)
    nombre_mois = echeance.duree
    acompte = None
    mensualite = None
    note = None
    if formule.lower().startswith("formule a"):
        acompte  = total * Decimal(0.3)
        if formule.lower() == "formule a":
            mensualite = total - acompte
            note = "RAC payable en 3ème mois"
        else:
            mensualite = (total - acompte) / (nombre_mois - 1)
    else:
        acompte = formation.acompte
        mensualite = (total - acompte) / nombre_mois
    return {
            "formule" : formule,
            "nombre_mois" : nombre_mois,
            "acompte" : acompte,
            "mensualite" : mensualite,
            "note" : note
            }

@login_required
def details_get(request, code):
    formation = None
    prerequis_scolaires = None
    prerequis_techniques = None
    organismes_emploi = None
    evolutions = None
    missions = None        
    qualites_requis = None
    avantages = None
    echeances = None
    tarifs = None

    try:
        formation = Formation.objects.get(code_formation=code)
    except:
        return render(request, "details/details.html")
 
    if formation.prerequis_scolaires:
        prerequis_scolaires = formation.prerequis_scolaires.all()
    if formation.prerequis_techniques:
        prerequis_techniques = formation.prerequis_techniques.all()
    if formation.organismes_emploi:
        organismes_emploi = formation.organismes_emploi.all()
    if formation.evolutions :
        evolutions = formation.evolutions.all()
    if formation.missions:
        missions = formation.missions.all()
    if formation.qualites_requis:
        qualites_requis = formation.qualites_requis.all()
    if formation.avantages:
        avantages = formation.avantages.all()

    tarifs = {
        "plain" : {
            "total" : formation.tarif_sans_acompte + formation.acompte,
            "echeances" : []
            },
        "minus15" : {
            "total" : (formation.tarif_sans_acompte + formation.acompte) * Decimal(0.85),
            "echeances" : []
            },
        "minus25" : {
            "total" : (formation.tarif_sans_acompte + formation.acompte) * Decimal(0.75),
            "echeances" : []
            }
        }

    for echeance in formation.echeances_tarif_plain.all():
        tarifs["plain"]["echeances"].append(calculateur_tarifs(formation, echeance, 0))
    for echeance in formation.echeances_tarif_minus15.all():
        tarifs["minus15"]["echeances"].append(calculateur_tarifs(formation, echeance, 0.15))
    for echeance in formation.echeances_tarif_minus25.all():
        tarifs["minus25"]["echeances"].append(calculateur_tarifs(formation, echeance, 0.25))
            
    return render(request, "details/details.html", {
        'formation' : formation,
        'prerequis_scolaires' : prerequis_scolaires,
        'prerequis_techniques' : prerequis_techniques,
        'organismes_emploi' : organismes_emploi,
        'evolutions' : evolutions,
        'missions' : missions,
        'qualites_requis' : qualites_requis,
        'avantages' : avantages,
        'tarifs' : tarifs
    })

@login_required
def details_post(request):
    try:
        code = request.POST["code_formation"]
        return redirect("details_get", code)
    except:
        return redirect('index')

def database_fill(request):
    ### add type formation 
    t_qualif = TypeFormation(description="Qualifiante")
    t_certif = TypeFormation(description="Certifiante")
    t_dipl = TypeFormation(description="Diplômante")
    t_qualif.save()
    t_certif.save()
    t_dipl.save()

    ### branche
    filename = "branches.csv"
    with open("static/files/" + filename, "r") as file:
        for line in file:
            b = BrancheFormation(description = line.strip())
            b.save()

    ### echeance
    filename = "echance.csv"
    sep = "§"
    file = open("static/files/" + filename, "r")
    file.readline()
    for line in file:
        code = line.split(sep)[0]
        duree = int(line.split(sep)[1]) 
        e = Echeance(code_echeance = code, duree = duree)
        e.save()
    file.close()

    ### formations and attestations
    filename = "formations.csv"
    file = open("static/files/" + filename, "r")
    file.readline()
    for line in file:
        intitule = line.split("§")[1]
        typeF = None
        if line.split("§")[1].endswith("ualifiant"):
            n = len(line.split("§")[1]) - len(" - Qualifiant")
            intitule = line.split("§")[1][:n]
            typeF = TypeFormation.objects.get(description="Qualifiante")
        elif line.split("§")[1].startswith("Titre"):
            typeF = TypeFormation.objects.get(description="Certifiante")
        else:
            typeF = TypeFormation.objects.get(description="Diplômante")

        stage = int(line.split("§")[5].split()[0]) if line.split("§")[5] != "N.O" else 0
        lien_cpf = line.split("§")[6] if line.split("§")[6] != "N.A" else None

        attestation = None
        try:
            attestation = AttestationFormation.objects.get(description=line.split("§")[4])
        except:
            attestation = AttestationFormation(description=line.split("§")[4])
            attestation.save()

        e = Formation(code_formation = int(line.split("§")[0]), intitule_formation = intitule, type_formation = typeF, duree_formation_mois = int(line.split("§")[2]), duree_formation_heures = int(line.split("§")[3]), attestation_formation = attestation, duree_stage_semaines = stage, lien_cpf=lien_cpf, tarif_sans_acompte = float(line.split("§")[7]) - 55, acompte = 55.0, lien_brochure = line.split("§")[9], branche_formation = BrancheFormation.objects.get(description = line.split("§")[10].strip()))

        e.save()

    file.close()

    ### echeances formation
    filename = "echeances_plain.csv"
    sep = "§"
    with open("static/files/" + filename, "r") as file:
        file.readline()
        for line in file:
            f = Formation.objects.get(code_formation=int(line.split(sep)[0][:4]))
            f.echeances_tarif_plain.add(Echeance.objects.get(code_echeance=line.split(sep)[1][:-1]))
            f.save()

    filename = "echeances_15.csv"
    sep = "§"
    with open("static/files/" + filename, "r") as file:
        file.readline()
        for line in file:
            f = Formation.objects.get(code_formation=int(line.split(sep)[0][:4]))
            f.echeances_tarif_minus15.add(Echeance.objects.get(code_echeance=line.split(sep)[1][:-1]))
            f.save()

    filename = "echeances_25.csv"
    sep = "§"
    with open("static/files/" + filename, "r") as file:
        file.readline()
        for line in file:
            f = Formation.objects.get(code_formation=int(line.split(sep)[0][:4]))
            f.echeances_tarif_minus25.add(Echeance.objects.get(code_echeance=line.split(sep)[1][:-1]))
            f.save()


    ### insert others
    others = [
            {
                "filename" : "prerequis_scolaire",
                "class" : PrerequisScolaire,
                "sep" : "§"
                },{
                "filename" : "prerequis_technique",
                "class" : PrerequisTechnique,
                "sep" : ","
                },{
                "filename" : "evolutions",
                "class" : EvolutionFormation,
                "sep" : "§"
                },{
                "filename" : "missions",
                "class" : MissionFormation,
                "sep" : "§"
                },{
                "filename" : "avantages",
                "class" : AvantageFormation,
                "sep" : "§"
                },{
                "filename" : "qualites_requis",
                "class" : QualiteRequisFormation,
                "sep" : "§"
                },{
                "filename" : "organisme_emploi",
                "class" : OrganismeEmploiFormation,
                "sep" : "§"
                },
            ]
    for other in others:
        with open("static/files/" + other["filename"] + '.csv') as file:
            file.readline()
            sep = other["sep"]
            current_model = other["class"]
            for line in file:
                f = Formation.objects.get(code_formation = int(line.split(sep)[0]))
                elm = current_model(formation = f, description = line.split(sep)[1])
                elm.save()

    return HttpResponse('done')
