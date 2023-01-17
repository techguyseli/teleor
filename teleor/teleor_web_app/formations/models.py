from django.db import models

class TypeFormation(models.Model):
    description = models.CharField(max_length=250, primary_key=True)

class BrancheFormation(models.Model):
    description = models.CharField(max_length=250, primary_key=True)

class AttestationFormation(models.Model):
    description = models.CharField(max_length=250, primary_key=True)

class Echeance(models.Model):
    code_echeance = models.CharField(primary_key=True, max_length=250)
    duree = models.PositiveIntegerField()
    class Meta:
        constraints = [
                models.CheckConstraint(check=models.Q(duree__gt=0), name='duree_gt_0'),
                ]

class Formation(models.Model):
    code_formation = models.PositiveIntegerField(primary_key=True)
    intitule_formation = models.CharField(max_length=500)
    type_formation = models.ForeignKey('TypeFormation', on_delete=models.SET_NULL, null=True, related_name="formations")
    branche_formation = models.ForeignKey('BrancheFormation', on_delete=models.SET_NULL, null=True, related_name="formations")
    duree_formation_mois = models.PositiveIntegerField()
    duree_formation_heures = models.PositiveIntegerField()
    attestation_formation = models.ForeignKey('AttestationFormation', on_delete=models.SET_NULL, null=True, related_name="formations")
    duree_stage_semaines = models.PositiveIntegerField()
    lien_cpf = models.URLField(null=True, blank=True)
    tarif_sans_acompte = models.DecimalField(max_digits=7, decimal_places=2)
    acompte = models.DecimalField(max_digits=7, decimal_places=2)
    lien_brochure = models.URLField()
    echeances_tarif_plain = models.ManyToManyField(Echeance, related_name="formations_plain")
    echeances_tarif_minus15 = models.ManyToManyField(Echeance, related_name="formations_minus15")
    echeances_tarif_minus25 = models.ManyToManyField(Echeance, related_name="formations_minus25")
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(duree_formation_mois__gt=0) & models.Q(duree_formation_heures__gt=0), name='duree_formation_gte_0'),
            models.CheckConstraint(check=models.Q(tarif_sans_acompte__gt=0) & models.Q(acompte__gt=0), name='prix_gt_0')
                ]

class PrerequisScolaire(models.Model):
    description = models.CharField(max_length=2000)
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="prerequis_scolaires")

class PrerequisTechnique(models.Model):
    description = models.CharField(max_length=2000)
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="prerequis_techniques")

class EvolutionFormation(models.Model):
    description = models.CharField(max_length=2000)
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="evolutions")

class MissionFormation(models.Model):
    description = models.CharField(max_length=2000)
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="missions")

class AvantageFormation(models.Model):
    description = models.CharField(max_length=2000)
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="avantages")

class QualiteRequisFormation(models.Model):
    description = models.CharField(max_length=2000)
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="qualites_requis")

class OrganismeEmploiFormation(models.Model):
    description = models.CharField(max_length=2000)
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="organismes_emploi")
    

